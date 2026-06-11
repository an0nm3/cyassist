---
source: rss/nviso-labs
title: ConsentFix (a.k.a. AuthCodeFix): Detecting OAuth2 Authorization Code Phishing
url: https://blog.nviso.eu/2026/01/29/consentfix-a-k-a-authcodefix-detecting-oauth2-authorization-code-phishing/
date: 2026-01-29
item_id: https://blog.nviso.eu/2026/01/29/consentfix-a-k-a-authcodefix-detecting-oauth2-authorization-code-phishing/
category: techniques---

**Source:** NVISO Labs
**Link:** https://blog.nviso.eu/2026/01/29/consentfix-a-k-a-authcodefix-detecting-oauth2-authorization-code-phishing/

ConsentFix (a.k.a.AuthCodeFix) is the latest variant of the fix-type phishing attacks, initially identified by Push Security. In this technique, the adversary tricks the victim into generating an OAuth authorization code that is part of a localhost URL, by signing in to the Azure CLI instance (or other vulnerable applications). Then, the victim is instructed to copy that URL and paste it into a phishing website, essentially handing over the authorization code to the adversary, who is now able to exchange it for an access token. Using the access token, the adversary gets access to the victim's Microsoft account.
