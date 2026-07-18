#!/usr/bin/env python3
"""Build Cyassist v3 User Manual PDF — cyber-blue theme, ASCII logo as image."""
import os, re, base64, io
from pathlib import Path
import mistune
from mistune.plugins import table as md_table
from weasyprint import HTML
from PIL import Image, ImageDraw, ImageFont

SRC_MD = Path(__file__).parent / "CYASSIST_USER_MANUAL.md"
FONT_OTF = Path("/home/kali/bugbounty/Cambridge.otf")
OUT_PDF = Path("/home/kali/bugbounty/Cyassist_v3_User_Manual.pdf")

with open(SRC_MD, 'r') as f:
    md_content = f.read()

md = mistune.create_markdown(renderer='html', plugins=[md_table.table])
body_html = md(md_content)

# ── Render ASCII logo as PNG via PIL (exact pixel alignment) ────
LOGO_LINES = [
    "\u2584\u2580\u2580\u2580  \u2588   \u2588 \u2584\u2580\u2580\u2580\u2584 \u2584\u2580\u2580\u2580\u2580 \u2584\u2580\u2580\u2580\u2580  \u2580  \u2584\u2580\u2580\u2580\u2580 \u2580\u2580\u2588\u2580\u2580",
    "\u2588     \u2580\u2584 \u2584\u2580 \u2588\u2580\u2580\u2580\u2588  \u2580\u2580\u2580\u2584  \u2580\u2580\u2580\u2584  \u2588   \u2580\u2580\u2580\u2584   \u2588",
    " \u2580\u2580\u2580    \u2588   \u2580   \u2580 \u2580\u2580\u2580\u2580  \u2580\u2580\u2580\u2580   \u2580  \u2580\u2580\u2580\u2580    \u2580",
    "       \u2584\u2580",
]

def render_logo_image(font_size: int = 42, color: tuple = (0, 136, 255)) -> str:
    FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    font = ImageFont.truetype(FONT_MONO, font_size)
    
    max_chars = max(len(l) for l in LOGO_LINES)
    char_w = font.getbbox("M")[2]
    line_h = font.getbbox("M")[3] + 3
    
    # Inner padding around text + extra for box border
    inner_pad_x, inner_pad_y = 30, 20
    box_pad = 12  # extra border around the box
    
    text_w = char_w * max_chars
    text_h = line_h * len(LOGO_LINES)
    
    box_w = text_w + inner_pad_x * 2
    box_h = text_h + inner_pad_y * 2
    img_w = box_w + box_pad * 2
    img_h = box_h + box_pad * 2
    
    img = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # ── Background placeholder box ──────────────────────────────
    box_x0, box_y0 = box_pad, box_pad
    box_x1, box_y1 = box_x0 + box_w, box_y0 + box_h
    radius = 14
    
    # Outer glow ring
    for i in range(4):
        glow_alpha = 15 - i * 3
        off = i * 2
        draw.rounded_rectangle(
            [box_x0 - off, box_y0 - off, box_x1 + off, box_y1 + off],
            radius=radius + off,
            fill=(0, 136, 255, glow_alpha if glow_alpha > 0 else 1)
        )
    
    # Main box fill (dark semi-transparent)
    draw.rounded_rectangle(
        [box_x0, box_y0, box_x1, box_y1],
        radius=radius,
        fill=(8, 16, 34, 220),
        outline=(0, 120, 220, 120),
        width=1
    )
    
    # Inner subtle border
    inner = 3
    draw.rounded_rectangle(
        [box_x0 + inner, box_y0 + inner, box_x1 - inner, box_y1 - inner],
        radius=radius - 2,
        outline=(0, 150, 255, 40),
        width=1
    )
    
    # ── Render ASCII text ───────────────────────────────────────
    text_origin_x = box_x0 + inner_pad_x
    text_origin_y = box_y0 + inner_pad_y
    
    for li, line in enumerate(LOGO_LINES):
        x = text_origin_x
        y = text_origin_y + li * line_h
        for ch in line:
            # Soft glow
            for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                draw.text((x + dx, y + dy), ch, font=font, fill=(color[0], color[1], color[2], 55))
            # Main text
            draw.text((x, y), ch, font=font, fill=(color[0], color[1], color[2], 255))
            x += char_w
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f'data:image/png;base64,{b64}'

logo_data_uri = render_logo_image(42)



def font_data_uri(path):
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    ext = os.path.splitext(path)[1].lower()
    mime = {'otf': 'font/otf', 'ttf': 'font/ttf'}.get(ext, 'font/otf')
    return f'data:{mime};base64,{data}'

font_uri = font_data_uri(str(FONT_OTF))

# ── Strip title / TOC from source; inject section page breaks ─────
content_lines = body_html.split('\n')
filtered = []
skip_until_content = True
for line in content_lines:
    if '<h1>Cyassist v3' in line:
        continue
    if skip_until_content:
        if 'id="s1"' in line or '<h2>1. Overview' in line or '<h2>1.' in line:
            skip_until_content = False
            filtered.append(line)
        continue
    filtered.append(line)
body_html = '\n'.join(filtered)

# Inject page-break before each numbered h2 (1.–18. and Appendix)
body_html = re.sub(
    r'<h2>(\d+\. |Appendix)',
    r'<div class="section-break"></div>\n<h2>\1',
    body_html
)
# Remove break before section 1 (follows TOC)
body_html = body_html.replace('<div class="section-break"></div>\n<h2>1. ', '<h2>1. ', 1)
# Remove break before Appendix (follows sec 18)
body_html = body_html.replace('<div class="section-break"></div>\n<h2>Appendix:', '<h2>Appendix:', 1)

# ── TOC sub-items ──────────────────────────────────────────────────
toc_items = [
    ("1. Overview", [
        "What Makes Cyassist Different",
    ]),
    ("2. Architecture", [
        "Data Flow",
    ]),
    ("3. Installation", [
        "Prerequisites",
        "Setup",
        "CLI Wrapper",
    ]),
    ("4. Quick Start", [
        "Show database status",
        "Scrape Indian news",
        "Harvest exploit DNA",
        "Watch mode",
    ]),
    ("5. Command-Line Flags", []),
    ("6. Sub-Modules", []),
    ("7. Intel DB", [
        "Tables",
        "Storage Budget",
    ]),
    ("8. Indian News Scraping", []),
    ("9. Web News Scraping", []),
    ("10. Exploit DNA Harvesting", [
        "Exploit-DB RSS",
        "GitHub API",
        "Technique Classification",
    ]),
    ("11. Template Sync", [
        "Nuclei Templates",
        "Metasploit Modules",
    ]),
    ("12. Rudra Bridge", [
        "Tech → CVE Lookup",
        "CVE → Probe Config",
        "Auto-Scan Config",
        "Finding Enrichment",
        "Static Tech→CVE Map",
        "Target Import",
    ]),
    ("13. On-Demand Exploit Fetcher", [
        "From Exploit-DB",
        "From GitHub",
        "By CVE",
        "Nuclei On-Demand",
    ]),
    ("14. Watch Mode", [
        "Features",
        "Auto-Scan Mode",
    ]),
    ("15. Daily Auto-Run", [
        "Cron Setup",
    ]),
    ("16. Targets", [
        "Current Targets",
        "Add a Target",
    ]),
    ("17. Database Schema", []),
    ("18. False Positive Prevention", [
        "Never-Report List",
    ]),
]

toc_html = ''
for section, subs in toc_items:
    num = section.split(".")[0]
    toc_html += f'    <li class="toc-section"><a href="#s{num}">{section}</a></li>\n'
    if subs:
        toc_html += '    <ul class="toc-subs">\n'
        for sub in subs:
            toc_html += f'      <li><a href="#s{num}">{sub}</a></li>\n'
        toc_html += '    </ul>\n'

# ── Build full HTML template ──────────────────────────────────────
html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
  size: A4;
  margin: 55pt 60pt 50pt 60pt;
  background: #0a0e17;
  @bottom-center {{
    content: counter(page);
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 9pt;
    color: #556;
    vertical-align: middle;
  }}
}}

@page title-page {{
  background: #0a0e17;
  @bottom-center {{ content: none; }}
}}

@page manual-page {{
  background: #0a0e17;
  @bottom-center {{ content: none; }}
}}

@page toc-page {{
  background: #0a0e17;
  @bottom-center {{
    content: counter(page);
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 9pt;
    color: #556;
    vertical-align: middle;
  }}
}}

@font-face {{
  font-family: 'Cambridge';
  src: url({font_uri}) format('opentype');
  font-weight: normal;
}}

@font-face {{
  font-family: 'Cambridge';
  src: url({font_uri}) format('opentype');
  font-weight: bold;
}}

html {{
  margin: 0;
  padding: 0;
  background: #0a0e17;
}}

body {{
  margin: 0;
  padding: 0;
  font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
  font-size: 10.5pt;
  line-height: 1.55;
  color: #c5cdd9;
  background: transparent;
}}

/* ===== TITLE PAGE ===== */
.title-page {{
  page: title-page;
  page-break-after: always;
  text-align: center;
  padding: 0;
}}

.title-page .logo-img {{
  display: block;
  margin: 15pt auto 12pt;
  max-width: 85%;
  height: auto;
}}

.title-page .version-below-logo {{
  font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
  font-size: 28pt;
  color: #6f42c1;
  font-weight: bold;
  margin: 2pt 0 14pt;
  letter-spacing: 3pt;
}}

.title-page .gradient-line {{
  width: 60%;
  height: 2pt;
  margin: 0 auto 22pt;
  background: linear-gradient(90deg, rgba(0,136,255,0) 0%, #0088ff 15%, #00ddff 40%, #6f42c1 60%, #0088ff 85%, rgba(0,136,255,0) 100%);
  border: none;
}}

.title-page .subtitle {{
  margin-top: 0;
  font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
  font-size: 18pt;
  color: #00ddff;
  font-weight: bold;
  margin-bottom: 24pt;
  letter-spacing: 1.5pt;
}}

.title-page .tagline {{
  font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
  font-size: 12pt;
  color: #667;
  margin-bottom: 5pt;
}}

.title-page .author-name {{
  font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
  font-size: 16pt;
  color: #c5cdd9;
  font-weight: bold;
  margin-top: 35pt;
  margin-bottom: 4pt;
  letter-spacing: 1pt;
}}

.title-page .handle {{
  font-family: 'Courier New', 'Liberation Mono', monospace;
  font-size: 22pt;
  font-weight: bold;
  color: #00ddff;
  margin-bottom: 20pt;
}}

.title-page .footer-text {{
  font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
  font-size: 11pt;
  color: #445;
}}



/* ===== MANUAL TITLE PAGE ===== */
.manual-title-page {{
  page: manual-page;
  page-break-after: always;
  text-align: center;
  padding: 0;
}}

.manual-title-page .manual-title {{
  font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
  font-size: 26pt;
  font-weight: bold;
  color: #0088ff;
  margin-top: 180pt;
  letter-spacing: 1pt;
}}

/* ===== TOC PAGE ===== */
.toc-page {{
  page: toc-page;
  page-break-after: always;
  padding: 0;
}}

.toc-page h1 {{
  text-align: center;
  border: none;
  color: #0088ff;
  font-size: 18pt;
  margin-top: 6pt;
  margin-bottom: 12pt;
}}

.toc {{
  column-count: 2;
  column-gap: 20pt;
}}

.toc-section {{
  margin-top: 4pt;
  list-style: none;
}}

.toc-section a {{
  display: block;
  padding: 1.5pt 0;
  color: #00ddff;
  font-size: 9pt;
  text-decoration: none;
  font-weight: bold;
}}

.toc-subs {{
  margin: 0 0 1pt 4pt;
  padding-left: 10pt;
  list-style: none;
}}

.toc-subs li a {{
  display: block;
  padding: 0.8pt 0;
  color: #778;
  font-size: 7.8pt;
  text-decoration: none;
  font-weight: normal;
  line-height: 1.25;
}}

/* ===== CONTENT ===== */
.page-content {{
  padding: 0;
}}

h1, h2, h3, h4 {{
  font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
  color: #0088ff;
  font-weight: bold;
  page-break-after: avoid;
}}

h1 {{
  font-size: 22pt;
  margin: 8pt 0 14pt;
  color: #00aaff;
  border-bottom: 1pt solid #1a2740;
  padding-bottom: 6pt;
}}

.section-break {{
  page-break-after: always;
  height: 0;
  margin: 0;
  padding: 0;
  line-height: 0;
  font-size: 0;
}}

h2 {{
  font-size: 16pt;
  margin: 0 0 10pt;
  color: #0088ff;
  padding-top: 4pt;
}}

h3 {{
  font-size: 13pt;
  margin: 16pt 0 8pt;
  color: #00ddff;
}}

h4 {{
  font-size: 11pt;
  margin: 12pt 0 6pt;
  color: #6f42c1;
}}

p {{
  margin: 5pt 0;
  text-align: justify;
  color: #c5cdd9;
}}

a {{
  color: #00ddff;
  text-decoration: none;
}}

strong {{
  color: #6f42c1;
}}

em {{
  color: #778;
}}

blockquote {{
  margin: 10pt 16pt;
  padding: 6pt 12pt;
  border-left: 3pt solid #0088ff;
  background: #0d1520;
  color: #99a;
  font-style: italic;
}}

hr {{
  border: none;
  border-top: 1pt solid #1a2740;
  margin: 20pt 0;
}}

/* ===== CODE BLOCKS (cyan) ===== */
pre, code {{
  font-family: 'Courier New', 'Liberation Mono', monospace;
  font-size: 8.5pt;
}}

pre {{
  background: #0b111e;
  border: 1pt solid #1a2740;
  border-radius: 3pt;
  padding: 8pt 10pt;
  margin: 6pt 0;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-all;
  color: #00ddff;
  line-height: 1.35;
}}

code {{
  background: #121a2a;
  padding: 1pt 4pt;
  border-radius: 2pt;
  color: #00c8c8;
  font-size: 9pt;
}}

pre code {{
  background: none;
  padding: 0;
  color: #00ddff;
  font-size: inherit;
}}

/* ===== TABLES ===== */
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 12pt 0;
  font-size: 9pt;
  page-break-inside: auto;
}}

tr {{
  page-break-inside: avoid;
}}

th, td {{
  padding: 6pt 10pt;
  border: 1.5pt solid #2a3a55;
  text-align: left;
  vertical-align: top;
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
}}

th {{
  background: #0f1a2e;
  color: #00ddff;
  font-weight: bold;
  border-bottom: 2.5pt solid #0088ff;
}}

td {{
  background: #0a0e17;
  color: #bcc;
}}

tr:nth-child(even) td {{
  background: #0d1520;
}}

/* ===== LISTS ===== */
ul, ol {{
  margin: 4pt 0;
  padding-left: 22pt;
  color: #c5cdd9;
}}

li {{
  margin: 2pt 0;
}}

/* ===== UTILITIES ===== */
.text-center {{ text-align: center; }}
.text-muted {{ color: #667; }}
</style>
</head>
<body>

<!-- PAGE 1: TITLE PAGE -->
<div class="title-page">
  <img class="logo-img" src="{logo_data_uri}" alt="Cyassist" />
  <div class="version-below-logo">v3.0</div>
  <hr class="gradient-line" />
  <div class="subtitle">Engine-Driven Bug Bounty Assistant</div>
  <div class="tagline">SQLite-backed threat intel &bull; Indian-first news &bull; Rudra-native bridge</div>
  <div class="tagline">Metadata only &bull; Zero exploit code cached &bull; 8 Indian scrapers</div>
  <div class="author-name">Pinaki Ranjan Patra</div>
  <div class="handle">&lt; 4n0n0n3 &gt;</div>
  <div class="footer-text">Built for bug bounty intel gathering and authorized security research</div>
</div>

<!-- PAGE 2: MANUAL TITLE -->
<div class="manual-title-page">
  <div class="manual-title">Cyassist v3.0<br/>&mdash; User Manual</div>
</div>

<!-- PAGE 3: TABLE OF CONTENTS -->
<div class="toc-page">
  <h1>Table of Contents</h1>
  <ul class="toc" style="list-style:none; padding:0;">
{toc_html}
    <li class="toc-section" style="margin-top:10pt;"><a href="#sapp">Appendix A: File Reference</a></li>
    <ul class="toc-subs">
      <li><a href="#sapp">File sizes / Module descriptions</a></li>
    </ul>
    <li class="toc-section"><a href="#sappb">Appendix B: Storage Budget Tracking</a></li>
  </ul>
</div>

<!-- CONTENT SECTIONS -->
<div class="page-content">
{body_html}
</div>

</body>
</html>'''

print("Building Cyassist v3 User Manual PDF ...")
HTML(string=html_template).write_pdf(str(OUT_PDF))
print(f"  {OUT_PDF.name} — {os.path.getsize(str(OUT_PDF)) / 1024:.0f}KB")
