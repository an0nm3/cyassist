"""Phase G: Adaptive Crawler — Playwright-based SPA crawling with login automation.

Four components:
  G1: Enhanced SPA crawling — click buttons, submit forms, scroll, lazy load
  G2: Login flow automation — detect forms, fill credentials, capture session
  G3: Stateful navigation — login → dashboard → settings, role-based trees
  G4: Auth-aware discovery — pre-auth vs post-auth surface comparison

Integrates with the Knowledge Graph to store discovered surfaces with
auth annotations, tech stack, and framework detection.
"""

import json
import logging
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from urllib.parse import urljoin, urlparse

from engine.knowledge_graph import (
    KnowledgeGraph,
    NODE_SURFACE,
    NODE_SESSION,
    EDGE_RUNS_ON,
    EDGE_LEADS_TO,
    EDGE_REQUIRES_AUTH,
    make_surface_node,
)

logger = logging.getLogger("adaptive_crawler")

try:
    from playwright.sync_api import sync_playwright, Page, Route, Request, ElementHandle
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


# ── Auth State Enum ──────────────────────────────────────────────────

class AuthState(Enum):
    UNKNOWN = "unknown"
    PRE_AUTH = "pre_auth"
    LOGGING_IN = "logging_in"
    AUTHENTICATED = "authenticated"
    LOGIN_FAILED = "login_failed"
    SESSION_EXPIRED = "session_expired"


# ── Data Classes ─────────────────────────────────────────────────────

@dataclass
class DiscoveredRoute:
    path: str
    method: str = "GET"
    auth_required: bool = False
    role: str = ""
    tech: list[str] = field(default_factory=list)
    framework: str = ""
    content_type: str = ""
    status: int = 0
    source: str = "crawl"  # "crawl", "login_redirect", "form_discovery"
    params: list[str] = field(default_factory=list)
    response_keys: list[str] = field(default_factory=list)


@dataclass
class LoginForm:
    url: str
    username_selector: str = ""
    password_selector: str = ""
    submit_selector: str = ""
    extra_fields: dict = field(default_factory=dict)
    action_url: str = ""
    method: str = "POST"
    detected_by: str = ""  # "password_field", "login_text", "known_path"


@dataclass
class AuthSession:
    cookies: list[dict] = field(default_factory=list)
    headers: dict = field(default_factory=dict)
    bearer_token: str = ""
    storage_state: dict = field(default_factory=dict)
    auth_type: str = ""  # "cookie", "bearer", "basic", "oauth"
    expires_at: float = 0.0
    created_at: float = 0.0


@dataclass
class CrawlResult:
    url: str
    pre_auth_surfaces: list[DiscoveredRoute] = field(default_factory=list)
    post_auth_surfaces: list[DiscoveredRoute] = field(default_factory=list)
    authenticated: bool = False
    auth_type: str = ""
    login_form: Optional[LoginForm] = None
    login_success: bool = False
    total_routes: int = 0
    api_endpoints: list[str] = field(default_factory=list)
    graphql_operations: list[dict] = field(default_factory=list)
    websocket_urls: list[str] = field(default_factory=list)
    js_bundles: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    duration_ms: float = 0.0


# ── Adaptive Crawler ─────────────────────────────────────────────────

class AdaptiveCrawler:
    """Playwright-based adaptive crawler with login automation.

    Usage:
        crawler = AdaptiveCrawler("https://target.com")
        result = crawler.crawl()
        # result.pre_auth_surfaces — routes found before login
        # result.post_auth_surfaces — routes found after login
        # result.authenticated — whether login succeeded

    Integrates with Knowledge Graph:
        surfaces = crawler.to_knowledge_graph_nodes()
        for surface in surfaces:
            kg.add_node(surface)
    """

    # Selectors for login form detection
    _LOGIN_SELECTORS = [
        "input[type='password']",
        "input[name*='password' i]",
        "input[name*='pass' i][type='text']",
        "input[name*='login' i]",
        "input[name*='username' i]",
        "input[name*='email' i][type='email']",
        "input[name*='user' i]",
        "button[type='submit']",
        "button:has-text('Sign In')",
        "button:has-text('Log In')",
        "button:has-text('Login')",
        "button:has-text('Sign in')",
        "button:has-text('Log in')",
        "a:has-text('Sign In')",
        "a:has-text('Log In')",
        "a:has-text('Login')",
        "[aria-label*='login' i]",
        "[aria-label*='sign in' i]",
        "form:has(input[type='password'])",
    ]

    # Known login paths
    _LOGIN_PATHS = [
        "/login", "/signin", "/sign-in", "/log-in",
        "/login.php", "/signin.php", "/sign-in.php",
        "/auth/login", "/account/login", "/user/login",
        "/auth/login.php", "/account/login.php", "/user/login.php",
        "/api/auth/login", "/api/v1/auth/login",
        "/sso/login", "/oauth/authorize",
        "/wp-login.php", "/admin/login", "/administrator",
    ]

    # Common post-login redirect paths
    _POST_LOGIN_PATHS = [
        "/dashboard", "/home", "/account", "/profile",
        "/settings", "/admin", "/app", "/portal",
        "/my-account", "/me", "/user/profile",
        "/setup.php", "/index.php", "/welcome",
    ]

    _CHROMIUM_PATHS = [
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
    ]

    def __init__(
        self,
        target_url: str,
        credentials: Optional[dict] = None,
        max_routes: int = 30,
        max_depth: int = 3,
        timeout_ms: int = 30000,
        headless: bool = True,
        cookies: Optional[list[dict]] = None,
        kg: Optional[KnowledgeGraph] = None,
    ):
        self.target_url = target_url
        self.credentials = credentials or {}
        self.max_routes = max_routes
        self.max_depth = max_depth
        self.timeout_ms = timeout_ms
        self.headless = headless
        self.cookies = cookies or []
        self.kg = kg or KnowledgeGraph()

        self._auth_state = AuthState.UNKNOWN
        self._session: Optional[AuthSession] = None
        self._pre_auth_routes: dict[str, DiscoveredRoute] = {}
        self._post_auth_routes: dict[str, DiscoveredRoute] = {}
        self._visited_paths: set[str] = set()

    # ── G4: Auth-Aware Crawl Entry Point ────────────────────────────

    def crawl(self) -> CrawlResult:
        """Execute full adaptive crawl: pre-auth → login → post-auth."""
        if not HAS_PLAYWRIGHT:
            return CrawlResult(
                url=self.target_url,
                errors=["Playwright not available"],
            )

        result = CrawlResult(url=self.target_url)
        start = time.time()

        try:
            with sync_playwright() as pw:
                launch_opts = {"headless": self.headless}
                chromepath = self._find_chromium()
                if chromepath:
                    launch_opts["executable_path"] = chromepath
                browser = pw.chromium.launch(**launch_opts)
                context = browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent=(
                        "Mozilla/5.0 (X11; Linux x86_64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/148.0.0.0 Safari/537.36"
                    ),
                    ignore_https_errors=True,
                )

                if self.cookies:
                    context.add_cookies(self.cookies)

                page = context.new_page()

                # ── Phase 1: Pre-auth crawl (G1) ────────────────────
                logger.info("Phase 1: Pre-auth crawl")
                self._crawl_pre_auth(page, result)

                # ── Phase 2: Login flow (G2) ────────────────────────
                logger.info("Phase 2: Login automation")
                self._attempt_login(page, context, result)

                # ── Phase 3: Post-auth crawl (G3) ───────────────────
                if self._auth_state == AuthState.AUTHENTICATED:
                    logger.info("Phase 3: Post-auth stateful crawl")
                    self._crawl_post_auth(page, context, result)

                # ── Phase 4: Compare surfaces (G4) ──────────────────
                logger.info("Phase 4: Auth-aware comparison")
                self._compare_surfaces(result)

                context.close()
                browser.close()

        except Exception as e:
            result.errors.append(f"Crawl failed: {e}")
            logger.error("Crawl error: %s", e)

        result.duration_ms = (time.time() - start) * 1000
        result.total_routes = len(result.pre_auth_surfaces) + len(result.post_auth_surfaces)

        # Auto-integrate with Knowledge Graph
        self.to_knowledge_graph_nodes(result)

        logger.info(
            "Crawl complete: %d pre-auth, %d post-auth, auth=%s, %d endpoints",
            len(result.pre_auth_surfaces),
            len(result.post_auth_surfaces),
            result.authenticated,
            len(result.api_endpoints),
        )
        return result

    # ── G1: Enhanced SPA Crawling ──────────────────────────────────

    @staticmethod
    def _find_chromium() -> Optional[str]:
        """Find a working chromium executable."""
        for path in AdaptiveCrawler._CHROMIUM_PATHS:
            import os
            if os.path.exists(path):
                return path
        return None

    def _crawl_pre_auth(self, page: Page, result: CrawlResult):
        """Crawl surfaces accessible without authentication."""
        self._auth_state = AuthState.PRE_AUTH
        api_urls: set[str] = set()
        ws_urls: set[str] = set()
        gql_ops: list[dict] = []
        js_bundles: list[str] = []

        def _on_request(request: Request):
            url = request.url
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https"):
                if parsed.scheme in ("ws", "wss"):
                    ws_urls.add(url)
                return
            if any(ext in url for ext in (".js", ".css", ".png", ".jpg", ".svg")):
                if ".js" in url:
                    js_bundles.append(url)
                return
            if "/api/" in url or "/rest/" in url or "/graphql" in url:
                api_urls.add(url)
            if "graphql" in url.lower() or "gql" in url.lower():
                self._capture_graphql(request, gql_ops)

        page.on("request", _on_request)

        # Navigate to target
        try:
            resp = page.goto(self.target_url, wait_until="networkidle", timeout=self.timeout_ms)
            initial_status = resp.status if resp else 0
        except Exception as e:
            result.errors.append(f"Initial navigation failed: {e}")
            initial_status = 0

        # Extract current route
        self._extract_current_route(page, result.pre_auth_surfaces, initial_status)

        # Discover and follow links (G1)
        self._discover_and_follow_links(page, result.pre_auth_surfaces, api_urls)

        # G1: Interact with page elements (buttons, forms, lazy load)
        self._interact_with_elements(page, result.pre_auth_surfaces, api_urls)

        # G1: Scroll for lazy loading
        self._scroll_for_lazy_load(page, result.pre_auth_surfaces, api_urls)

        # Store discovered API endpoints
        result.api_endpoints = list(api_urls)
        result.websocket_urls = list(ws_urls)
        result.graphql_operations = gql_ops
        result.js_bundles = js_bundles

        # Remove listener
        try:
            page.remove_listener("request", _on_request)
        except Exception:
            pass

    def _discover_and_follow_links(
        self, page: Page, surfaces: list, api_urls: set
    ):
        """Discover links on the page and follow them up to max_routes."""
        current_url = page.url
        parsed_current = urlparse(current_url)
        parsed_target = urlparse(self.target_url)

        links = page.eval_on_selector_all(
            "a[href]",
            """els => els.map(el => ({
                href: el.getAttribute('href'),
                text: (el.textContent || '').trim().toLowerCase().substring(0, 50)
            })).filter(l => l.href && !l.href.startsWith('#')
                    && !l.href.startsWith('mailto:')
                    && !l.href.startsWith('tel:'))"""
        )

        for link in links:
            if len(self._visited_paths) >= self.max_routes:
                break

            resolved = urljoin(current_url, link["href"])
            parsed_link = urlparse(resolved)

            if parsed_link.netloc and parsed_link.netloc != parsed_current.netloc:
                continue
            if parsed_link.netloc and parsed_link.netloc != parsed_target.netloc:
                continue

            path = parsed_link.path or "/"
            if path in self._visited_paths:
                continue
            self._visited_paths.add(path)

            # Skip static assets
            if any(path.endswith(ext) for ext in (".js", ".css", ".png", ".jpg", ".svg", ".ico")):
                continue

            try:
                resp = page.goto(resolved, wait_until="networkidle", timeout=self.timeout_ms)
                status = resp.status if resp else 0
                route = DiscoveredRoute(
                    path=path,
                    method="GET",
                    status=status,
                    source="link_follow",
                )
                self._extract_tech_from_page(page, route)
                surfaces.append(route)

                # G1: On each new page, try to interact and scroll
                self._interact_with_elements(page, surfaces, api_urls)
                self._scroll_for_lazy_load(page, surfaces, api_urls)
            except Exception:
                continue

    def _interact_with_elements(
        self, page: Page, surfaces: list, api_urls: set
    ):
        """G1: Click interactive elements to discover hidden routes."""
        # Click buttons that might reveal content (e.g., "Show more", "Expand")
        buttons = page.query_selector_all(
            "button:not([type='submit']):not([aria-hidden='true']), "
            "a[role='button'], "
            "[onclick], "
            ".accordion-header, .expand-button, .toggle"
        )
        for btn in buttons[:5]:
            try:
                text = (btn.text_content() or "").strip().lower()
                # Skip navigation/trivial buttons
                if text in ("", "menu", "close", "x"):
                    continue
                btn.click()
                page.wait_for_timeout(1000)
                # Check if new content appeared
                self._extract_current_route(page, surfaces)
            except Exception:
                continue

    def _scroll_for_lazy_load(
        self, page: Page, surfaces: list, api_urls: set
    ):
        """G1: Scroll page to trigger lazy-loaded content."""
        try:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1500)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(500)
        except Exception:
            pass

    # ── G2: Login Flow Automation ──────────────────────────────────

    def _detect_login_form(self, page: Page) -> Optional[LoginForm]:
        """Detect a login form on the current page.

        Looks for password fields, login-associated text, and known paths.
        """
        current_url = page.url

        # Check if we're on a known login path
        parsed = urlparse(current_url)
        for login_path in self._LOGIN_PATHS:
            if login_path in parsed.path:
                logger.info("Login page detected via path: %s", parsed.path)

        # Find password field (strongest signal)
        pw_field = page.query_selector("input[type='password']")
        if not pw_field:
            # Try alternate selectors
            pw_field = page.query_selector(
                "input[name*='password' i], input[type='password']"
            )

        if not pw_field:
            return None

        form = LoginForm(url=current_url, detected_by="password_field")

        # Find the form element
        form_element = page.evaluate("""(el) => {
            const form = el.closest('form');
            return form ? {
                action: form.getAttribute('action') || '',
                method: (form.getAttribute('method') || 'POST').toUpperCase()
            } : null;
        }""", pw_field)

        if form_element:
            form.action_url = urljoin(current_url, form_element.get("action", ""))
            form.method = form_element.get("method", "POST")

        # Find username field
        username_selectors = [
            "input[name*='email' i]",
            "input[name*='username' i]",
            "input[name*='login' i]",
            "input[name*='user' i]",
            "input[type='email']",
            "input[type='text']:not([name*='search' i])",
        ]
        for sel in username_selectors:
            field = page.query_selector(sel)
            if field:
                name = field.get_attribute("name") or field.get_attribute("id") or ""
                if name and "password" not in name.lower():
                    form.username_selector = sel
                    break

        # Default to first text input if no username field found
        if not form.username_selector:
            first_text = page.query_selector("input[type='text']")
            if first_text:
                form.username_selector = "input[type='text']"

        # Find password selector
        form.password_selector = "input[type='password']"

        # Find submit button
        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Sign In')",
            "button:has-text('Log In')",
            "button:has-text('Login')",
            "button:has-text('Sign in')",
            "button:has-text('Submit')",
        ]
        for sel in submit_selectors:
            btn = page.query_selector(sel)
            if btn:
                form.submit_selector = sel
                break

        # Check for extra hidden fields
        extra = page.evaluate("""() => {
            const inputs = document.querySelectorAll('input[type="hidden"]');
            const result = {};
            inputs.forEach(i => {
                const name = i.getAttribute('name');
                const value = i.getAttribute('value') || '';
                if (name) result[name] = value;
            });
            return result;
        }""")
        if extra:
            form.extra_fields = extra

        return form

    def _attempt_login(
        self, page: Page, context, result: CrawlResult
    ):
        """Attempt automated login using detected credentials or defaults."""
        if not self.credentials.get("username") and not self.credentials.get("password"):
            logger.info("No credentials provided — skipping login")
            return

        parsed_target = urlparse(self.target_url)

        # Strategy 1: Check if current page already has a login form
        current_url = page.url
        form = self._detect_login_form(page)
        if form:
            logger.info("Login form detected on current page: %s", current_url)
            result.login_form = form
            success = self._fill_and_submit_login(page, form, context)
            if success:
                result.authenticated = True
                result.auth_type = self._session.auth_type if self._session else "cookie"
                return

        # Strategy 2: Try known login paths
        for login_path in self._LOGIN_PATHS:
            login_url = f"{parsed_target.scheme}://{parsed_target.netloc}{login_path}"
            try:
                resp = page.goto(login_url, wait_until="networkidle", timeout=self.timeout_ms)
                status = resp.status if resp else 0
                if status not in (200, 401, 403):
                    continue

                form = self._detect_login_form(page)
                if form:
                    result.login_form = form
                    success = self._fill_and_submit_login(page, form, context)
                    if success:
                        result.authenticated = True
                        result.auth_type = self._session.auth_type if self._session else "cookie"
                        return
            except Exception as e:
                logger.debug("Login attempt at %s failed: %s", login_path, e)

        # Strategy 3: Look for login links on homepage
        if not result.authenticated:
            logger.info("No login page found at known paths — scanning homepage for login links")
            try:
                page.goto(self.target_url, wait_until="networkidle", timeout=self.timeout_ms)
                login_links = page.eval_on_selector_all(
                    "a[href*='login' i], a[href*='signin' i], a[href*='auth' i]",
                    """els => els.map(el => el.getAttribute('href'))
                               .filter(h => h !== null)"""
                )
                for link in login_links[:3]:
                    resolved = urljoin(self.target_url, link)
                    try:
                        resp = page.goto(resolved, wait_until="networkidle", timeout=self.timeout_ms)
                        status = resp.status if resp else 0
                        if status not in (200, 401, 403):
                            continue
                        form = self._detect_login_form(page)
                        if form:
                            result.login_form = form
                            success = self._fill_and_submit_login(page, form, context)
                            if success:
                                result.authenticated = True
                                result.auth_type = self._session.auth_type if self._session else "cookie"
                                return
                    except Exception:
                        continue
            except Exception:
                pass

    def _fill_and_submit_login(
        self, page: Page, form: LoginForm, context
    ) -> bool:
        """Fill credentials into detected login form and submit."""
        self._auth_state = AuthState.LOGGING_IN

        username = self.credentials.get("username", "admin")
        password = self.credentials.get("password", "admin")

        try:
            # Fill username
            if form.username_selector:
                field = page.query_selector(form.username_selector)
                if field:
                    field.click()
                    field.fill(username)
                    page.wait_for_timeout(300)

            # Fill password
            if form.password_selector:
                field = page.query_selector(form.password_selector)
                if field:
                    field.click()
                    field.fill(password)
                    page.wait_for_timeout(300)

            # Extra hidden fields
            for name, value in form.extra_fields.items():
                try:
                    page.fill(f"input[name='{name}']", value)
                except Exception:
                    pass

            # Submit
            if form.submit_selector:
                btn = page.query_selector(form.submit_selector)
                if btn:
                    btn.click()
                else:
                    page.keyboard.press("Enter")
            else:
                page.keyboard.press("Enter")

            # Wait for navigation/response
            page.wait_for_timeout(3000)

            # Check if login succeeded
            current_url = page.url
            logged_in = False

            # Check for session cookie
            ctx_cookies = context.cookies()

            def _is_session_cookie(name: str) -> bool:
                nl = name.lower()
                # Check known session cookie names
                if nl in ("session", "sessionid", "connect.sid", "token", "jwt",
                          "bearer", "sid", "auth_token", "access_token",
                          "refresh_token", "phpsessid", "aspsessionid",
                          "cfid", "cftoken", "jsessionid"):
                    return True
                # Heuristic: any cookie that looks like a session token
                # (not a UI preference) with value length > 10
                return False

            session_cookies = [c for c in ctx_cookies if _is_session_cookie(c.get("name", ""))]
            if not session_cookies:
                # Broader heuristic: any cookie set during login flow
                # that isn't an obvious preference cookie
                blacklist = {"cookieconsent", "cookie_notice_accepted", "seen_cookie_message"}
                session_cookies = [c for c in ctx_cookies
                                   if c.get("name", "").lower() not in blacklist
                                   and len(c.get("value", "")) >= 16]

            if session_cookies:
                logged_in = True
                self._session = AuthSession(
                    cookies=ctx_cookies,
                    auth_type="cookie",
                    created_at=time.time(),
                )
                for sc in session_cookies:
                    if sc.get("expires", 0):
                        self._session.expires_at = sc["expires"]
                logger.info("Login succeeded — session cookie captured")

            # Check for redirect to post-login page
            parsed = urlparse(current_url)
            for post_path in self._POST_LOGIN_PATHS:
                if post_path in parsed.path:
                    logged_in = True
                    if not self._session:
                        self._session = AuthSession(
                            cookies=ctx_cookies,
                            auth_type="cookie",
                            created_at=time.time(),
                        )
                    logger.info("Login succeeded — redirected to %s", parsed.path)
                    break

            # Check for bearer token in localStorage/sessionStorage
            if not logged_in:
                try:
                    storage = page.evaluate("""() => ({
                        local: {...localStorage},
                        session: {...sessionStorage}
                    })""")
                    for store_name, store in storage.items():
                        if isinstance(store, dict):
                            for k, v in store.items():
                                if any(t in k.lower() for t in ("token", "jwt", "bearer", "auth")):
                                    if not self._session:
                                        self._session = AuthSession(auth_type="bearer")
                                    self._session.bearer_token = v
                                    self._session.storage_state = storage
                                    logged_in = True
                                    logger.info("Login succeeded — bearer token found in %s", store_name)
                                    break
                except Exception:
                    pass

            if logged_in:
                self._auth_state = AuthState.AUTHENTICATED
                self._session.headers = {
                    k: v for k, v in page.evaluate("""() => {
                        const h = new Headers();
                        const result = {};
                        // Can't iterate Headers directly in evaluate
                        return result;
                    }""").items() if k
                }
                return True
            else:
                self._auth_state = AuthState.LOGIN_FAILED
                logger.warning("Login failed — no session cookie or redirect detected")
                return False

        except Exception as e:
            self._auth_state = AuthState.LOGIN_FAILED
            logger.error("Login form interaction error: %s", e)
            return False

    # ── G3: Stateful Post-Auth Navigation ──────────────────────────

    def _crawl_post_auth(self, page: Page, context, result: CrawlResult):
        """Crawl authenticated surfaces by navigating stateful trees."""
        api_urls: set[str] = set(result.api_endpoints)
        ws_urls: set[str] = set(result.websocket_urls)

        def _on_request(request: Request):
            url = request.url
            if "/api/" in url or "/rest/" in url or "/graphql" in url:
                api_urls.add(url)

        page.on("request", _on_request)

        # G3: First explore current page links (where login redirects us)
        self._discover_and_follow_links(page, result.post_auth_surfaces, api_urls)

        # G3: Then try common post-login paths
        parsed_target = urlparse(self.target_url)
        base = f"{parsed_target.scheme}://{parsed_target.netloc}"

        for post_path in self._POST_LOGIN_PATHS:
            if len(self._visited_paths) >= self.max_routes + 15:
                break

            full_url = f"{base}{post_path}"
            if post_path in self._visited_paths:
                continue
            self._visited_paths.add(post_path)

            try:
                resp = page.goto(full_url, wait_until="networkidle", timeout=self.timeout_ms)
                status = resp.status if resp else 0
                route = DiscoveredRoute(
                    path=post_path,
                    method="GET",
                    auth_required=True,
                    status=status,
                    source="post_auth_nav",
                )
                self._extract_tech_from_page(page, route)
                self._extract_auth_info(page, route)
                result.post_auth_surfaces.append(route)

                # G3: On each auth page, check for nested navigation
                self._explore_auth_tree(page, result.post_auth_surfaces, api_urls, depth=0)
            except Exception as e:
                logger.debug("Post-auth nav to %s failed: %s", post_path, e)
                continue

        # Also check discovered API endpoints after auth
        for api_url in list(api_urls):
            parsed_api = urlparse(api_url)
            api_path = parsed_api.path or "/"
            if api_path not in self._visited_paths:
                self._visited_paths.add(api_path)
                try:
                    resp = page.goto(api_url, wait_until="networkidle", timeout=self.timeout_ms)
                    status = resp.status if resp else 0
                    route = DiscoveredRoute(
                        path=api_path,
                        method="GET",
                        auth_required=True,
                        status=status,
                        source="api_post_auth",
                    )
                    result.post_auth_surfaces.append(route)
                except Exception:
                    pass

        result.api_endpoints = list(api_urls)

        # Remove listener
        try:
            page.remove_listener("request", _on_request)
        except Exception:
            pass

    def _explore_auth_tree(
        self, page: Page, surfaces: list, api_urls: set, depth: int
    ):
        """G3: Recursively explore navigation elements on authenticated pages."""
        if depth >= self.max_depth:
            return

        # Find navigation elements and settings/admin links
        nav_links = page.query_selector_all(
            "nav a[href], "
            "[role='navigation'] a[href], "
            ".nav a[href], "
            ".sidebar a[href], "
            ".menu a[href], "
            "a:has-text('Settings'), "
            "a:has-text('Admin'), "
            "a:has-text('Profile'), "
            "a:has-text('Account'), "
            "a:has-text('Dashboard')"
        )

        for link in nav_links[:8]:
            if len(self._visited_paths) >= self.max_routes + 25:
                break

            href = link.get_attribute("href")
            if not href or href.startswith("#") or href.startswith("mailto:"):
                continue

            resolved = urljoin(page.url, href)
            parsed_link = urlparse(resolved)
            path = parsed_link.path or "/"

            if path in self._visited_paths:
                continue
            self._visited_paths.add(path)

            try:
                resp = page.goto(resolved, wait_until="networkidle", timeout=self.timeout_ms)
                status = resp.status if resp else 0
                route = DiscoveredRoute(
                    path=path,
                    method="GET",
                    auth_required=True,
                    status=status,
                    source="auth_tree",
                )
                self._extract_tech_from_page(page, route)
                self._extract_auth_info(page, route)
                surfaces.append(route)

                # Recurse into next level
                self._explore_auth_tree(page, surfaces, api_urls, depth + 1)
            except Exception:
                continue

    # ── G4: Auth-Aware Surface Comparison ──────────────────────────

    def _compare_surfaces(self, result: CrawlResult):
        """Compare pre-auth and post-auth surfaces.

        Tags:
          - auth_gated: only accessible after login
          - always_public: accessible before and after login
          - post_auth_only: new routes discovered only after auth
        """
        pre_paths = {r.path for r in result.pre_auth_surfaces}
        post_paths = {r.path for r in result.post_auth_surfaces}

        # Routes that exist only after auth
        auth_only_paths = post_paths - pre_paths

        for route in result.post_auth_surfaces:
            if route.path in auth_only_paths:
                route.auth_required = True
                route.source = "auth_gated"
            else:
                route.source = "always_public"

        for route in result.pre_auth_surfaces:
            if route.path in post_paths:
                route.source = "always_public"
            else:
                route.source = "pre_auth_only"

        logger.info(
            "Auth comparison: %d pre-auth, %d post-auth, %d auth-gated",
            len(pre_paths), len(post_paths), len(auth_only_paths),
        )

    # ── Helper Methods ─────────────────────────────────────────────

    def _extract_current_route(self, page: Page, surfaces: list, status: int = 0):
        """Extract the current page URL as a discovered route."""
        current_url = page.url
        parsed = urlparse(current_url)
        path = parsed.path or "/"
        if path not in self._visited_paths:
            self._visited_paths.add(path)
            route = DiscoveredRoute(path=path, method="GET", source="page_nav", status=status)
            self._extract_tech_from_page(page, route)
            surfaces.append(route)

    def _extract_tech_from_page(self, page: Page, route: DiscoveredRoute):
        """Extract tech stack signals from page content."""
        try:
            title = page.title()
            if title:
                route.response_keys = [title]

            page_source = page.content()
            lower = page_source.lower()

            # Framework detection
            if "__next_data__" in lower:
                route.tech.append("nextjs")
                route.framework = "nextjs"
            if "_reactroot" in lower or "react." in lower:
                route.tech.append("react")
                if not route.framework:
                    route.framework = "react"
            if "vue." in lower or "vuejs" in lower:
                route.tech.append("vue")
                if not route.framework:
                    route.framework = "vue"
            if "angular." in lower or "ng-app" in lower:
                route.tech.append("angular")
                if not route.framework:
                    route.framework = "angular"
            if "wp-content" in lower or "wp-includes" in lower:
                route.tech.append("wordpress")
                if not route.framework:
                    route.framework = "wordpress"
            if "laravel" in lower and "csrf" in lower:
                route.tech.append("laravel")
                if not route.framework:
                    route.framework = "laravel"
            if "django" in lower and "csrf" in lower:
                route.tech.append("django")
                if not route.framework:
                    route.framework = "django"

            # Content type detection
            content_type = ""
            try:
                content_type = page.evaluate(
                    "document.querySelector('meta[charset]')?.getAttribute('charset') "
                    "|| document.contentType || ''"
                )
            except Exception:
                pass
            if content_type:
                route.content_type = content_type

        except Exception:
            pass

    def _extract_auth_info(self, page: Page, route: DiscoveredRoute):
        """Extract auth requirements from page content/headers."""
        try:
            # Check for auth-related content
            lower_content = page.content().lower()
            if "access denied" in lower_content or "unauthorized" in lower_content:
                route.auth_required = True
            if "admin" in lower_content.lower() and "login" not in lower_content.lower():
                route.role = "admin"
            if "settings" in page.url.lower():
                route.role = "user"
        except Exception:
            pass

    def _capture_graphql(self, request: Request, gql_ops: list):
        """Extract GraphQL operations from request body."""
        try:
            body = request.post_data or ""
            if body:
                payload = json.loads(body)
                if "query" in payload or "operationName" in payload:
                    gql_ops.append({
                        "url": request.url,
                        "operationName": payload.get("operationName", ""),
                        "operationType": (
                            "mutation" if "mutation" in payload.get("query", "")
                            else "query"
                        ),
                        "method": request.method,
                    })
        except (json.JSONDecodeError, ValueError):
            pass

    # ── Knowledge Graph Integration ────────────────────────────────

    def to_knowledge_graph_nodes(self, result: Optional[CrawlResult] = None) -> list:
        """Convert crawl results to Knowledge Graph Node objects.

        Creates Surface nodes with auth annotations, edge connections
        between related surfaces (LEADS_TO), and tech associations (RUNS_ON).
        """
        if result is None:
            return []

        nodes = []
        edges = []

        # Track paths for linking
        all_routes = result.pre_auth_surfaces + result.post_auth_surfaces
        seen_surfaces: set[str] = set()

        for route in all_routes:
            surface_id = f"{route.method}:{route.path}"
            if surface_id in seen_surfaces:
                continue
            seen_surfaces.add(surface_id)

            node = make_surface_node(
                route.path,
                method=route.method,
                requires_auth=route.auth_required,
                role=route.role or "",
                framework=route.framework or "",
                tech=route.tech or [],
                source=route.source,
                status=route.status,
                content_type=route.content_type,
            )
            nodes.append(node)

        # Create LEADS_TO edges for sequential routes
        for i in range(len(all_routes) - 1):
            src = f"{NODE_SURFACE}:{all_routes[i].method}:{all_routes[i].path}"
            tgt = f"{NODE_SURFACE}:{all_routes[i + 1].method}:{all_routes[i + 1].path}"
            if src != tgt:
                from engine.knowledge_graph import Edge, EDGE_LEADS_TO
                edges.append(Edge(
                    source=src,
                    target=tgt,
                    edge_type=EDGE_LEADS_TO,
                    properties={"crawl_order": i},
                ))

        self.kg.add_node_batch(nodes)
        self.kg.add_edge_batch(edges)

        return nodes

    def get_session_node(self) -> str:
        """Store auth session in Knowledge Graph and return UID."""
        if not self._session:
            return ""
        session_id = f"session:{self.target_url}"
        from engine.knowledge_graph import Node
        self.kg.add_node(
            Node(
                NODE_SESSION, session_id,
                {
                    "auth_type": self._session.auth_type,
                    "created_at": self._session.created_at,
                    "target_url": self.target_url,
                },
            )
        )
        return session_id


# ── Convenience API ──────────────────────────────────────────────────


def crawl_target(
    url: str,
    username: str = "",
    password: str = "",
    max_routes: int = 20,
    headless: bool = True,
) -> CrawlResult:
    """One-shot: crawl a target with login attempt and return results."""
    credentials = {}
    if username and password:
        credentials = {"username": username, "password": password}

    crawler = AdaptiveCrawler(
        target_url=url,
        credentials=credentials,
        max_routes=max_routes,
        headless=headless,
    )
    result = crawler.crawl()
    return result
