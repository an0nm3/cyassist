#!/usr/bin/env python3
"""Build Cyassist v2 User Manual PDF — matches Rudra PDF style."""
import os, re, base64, io
from pathlib import Path
import mistune
from mistune.plugins import table as md_table
from weasyprint import HTML
from PIL import Image, ImageDraw, ImageFont

SRC_MD = Path(__file__).parent / "CYASSIST_USER_MANUAL.md"
FONT_OTF = Path("/home/kali/bugbounty/Cambridge.otf")
OUT_PDF = Path("/home/kali/bugbounty/Cyassist_v2_User_Manual.pdf")

with open(SRC_MD, 'r') as f:
    md_content = f.read()

md = mistune.create_markdown(renderer='html', plugins=[md_table.table])
body_html = md(md_content)

# ── Generate gradient logo ──────────────────────────────────
def render_logo(font_path: str, text: str = "Cyassist", font_size: int = 120) -> str:
    font = ImageFont.truetype(font_path, font_size)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 40, 30
    img_w, img_h = tw + pad_x * 2, th + pad_y * 2
    img = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((pad_x - bbox[0], pad_y - bbox[1]), text, font=font, fill=(255, 255, 255, 255))
    gradient = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(gradient)
    for y in range(img_h):
        t = y / img_h
        if t < 0.3:
            r, g, b = 0, int(136 * (t / 0.3)), 255
        elif t < 0.6:
            r, g, b = 0, int(136 + 68 * ((t - 0.3) / 0.3)), 255
        elif t < 0.85:
            r, g, b = 0, int(204 + 51 * ((t - 0.6) / 0.25)), 255
        else:
            r, g, b = 51, 255, 255
        gdraw.line([(0, y), (img_w - 1, y)], fill=(r, g, b, 255))
    out = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
    out.paste(gradient, (0, 0), img)
    buf = io.BytesIO()
    out.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f'data:image/png;base64,{b64}'

logo_data_uri = render_logo(str(FONT_OTF), "Cyassist", 120)

def font_data_uri(path):
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    ext = os.path.splitext(path)[1].lower()
    mime = {'otf': 'font/otf', 'ttf': 'font/ttf'}.get(ext, 'font/otf')
    return f'data:{mime};base64,{data}'

font_uri = font_data_uri(str(FONT_OTF))

# ── Strip title / TOC from source; inject page breaks ─────
content_lines = body_html.split('\n')
filtered = []
skip_until_content = True
for line in content_lines:
    if '<h1>Cyassist v2' in line:
        continue
    if skip_until_content:
        if 'id="s1"' in line or '<h2>1. Overview' in line or '<h2>1.' in line:
            skip_until_content = False
            filtered.append(line)
        continue
    filtered.append(line)
body_html = '\n'.join(filtered)

body_html = re.sub(
    r'<h2>(\d+\. |Appendix)',
    r'</div><div class="section-break"><h2>\1',
    body_html
)
body_html = re.sub(
    r'<h3>',
    r'</div><div class="subsec-break"><h3>',
    body_html
)

# ── Full HTML document ─────────────────────────────────────
html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: A4;
    margin: 2cm 1.8cm;
    @bottom-center {{
      content: counter(page);
      font-family: 'ManualFont', sans-serif;
      font-size: 9pt;
      color: #888;
    }}
  }}
  @font-face {{
    font-family: 'ManualFont';
    src: url({font_uri}) format('opentype');
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: 'ManualFont', 'DejaVu Sans Mono', monospace;
    background: #0d1117;
    color: #c9d1d9;
    font-size: 10pt;
    line-height: 1.6;
  }}
  .cover {{
    text-align: center;
    padding: 80px 0 40px 0;
    page-break-after: always;
  }}
  .cover h1 {{
    font-size: 36pt;
    margin: 20px 0 10px 0;
    background: linear-gradient(135deg, #0088ff, #00ddff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }}
  .cover .subtitle {{
    font-size: 14pt;
    color: #8b949e;
    margin-bottom: 30px;
  }}
  .cover .meta {{ font-size: 10pt; color: #6e7681; }}
  .toc {{ page-break-after: always; }}
  .toc h2 {{ color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 6px; }}
  .toc a {{ color: #c9d1d9; text-decoration: none; display: block; padding: 2px 0; }}
  .toc a:hover {{ color: #58a6ff; }}
  h2 {{ color: #58a6ff; font-size: 16pt; margin-top: 24pt; border-bottom: 1px solid #21262d; padding-bottom: 4px; }}
  h3 {{ color: #79c0ff; font-size: 13pt; margin-top: 18pt; }}
  h4 {{ color: #a5d6ff; font-size: 11pt; }}
  p {{ margin: 6pt 0; }}
  a {{ color: #58a6ff; }}
  code {{ background: #161b22; padding: 1px 5px; border-radius: 3px; font-size: 9pt; color: #f0f6fc; }}
  pre {{
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 12px;
    overflow-x: auto;
    font-size: 8.5pt;
    line-height: 1.4;
    color: #e6edf3;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10pt 0;
    font-size: 9pt;
    page-break-inside: auto;
  }}
  th, td {{
    border: 1px solid #30363d;
    padding: 6px 10px;
    text-align: left;
  }}
  th {{ background: #161b22; color: #58a6ff; font-weight: bold; }}
  tr:nth-child(even) {{ background: #0d1117; }}
  tr:nth-child(odd) {{ background: #161b22; }}
  blockquote {{
    border-left: 4px solid #30363d;
    padding: 8px 16px;
    margin: 10pt 0;
    background: #161b22;
    color: #8b949e;
  }}
  ul, ol {{ margin: 6pt 0; padding-left: 24px; }}
  li {{ margin: 2pt 0; }}
  hr {{ border: none; border-top: 1px solid #21262d; margin: 16pt 0; }}
  .section-break {{ page-break-before: always; }}
  .subsec-break {{ page-break-before: auto; }}
  img {{ max-width: 100%; }}
</style>
</head>
<body>

<div class="cover">
  <img src="{logo_data_uri}" alt="Cyassist Logo" style="max-width:400px;">
  <h1>Cyassist v2</h1>
  <div class="subtitle">Intel-Driven Bug Bounty Assistant</div>
  <div class="meta">
    SQLite-backed &bull; Indian-first threat intel &bull; Rudra-native bridge<br>
    Storage: &lt;100MB &bull; Metadata only &bull; Zero exploit code cached
  </div>
</div>

<div class="toc">
<h2>Table of Contents</h2>
"""

# Build TOC from <h2> tags
toc_entries = []
for line in body_html.split('\n'):
    m = re.search(r'<h2[^>]*>(\d+\.\s*[^<]+|Appendix\s*[^<]+)</h2>', line)
    if m:
        anchor = m.group(1).lower().replace(' ', '-').replace('.', '').replace('--', '-').rstrip('-')
        toc_entries.append((m.group(1), anchor))
    m2 = re.search(r'<h2[^>]*>([^<]+)</h2>', line)
    if m2 and not m:
        txt = m2.group(1)
        if txt not in ('Cyassist v2', 'Table of Contents'):
            anchor = txt.lower().replace(' ', '-').replace('.', '').replace('--', '-').rstrip('-')
            toc_entries.append((txt, anchor))

for title, anchor in toc_entries:
    html_doc += f'<a href="#{anchor}">{title}</a>\n'

html_doc += "</div>\n" + body_html + "\n</body></html>"

HTML(string=html_doc).write_pdf(str(OUT_PDF))

size_kb = os.path.getsize(str(OUT_PDF)) / 1024
print(f"  {os.path.basename(str(OUT_PDF))} — {size_kb:.0f}KB")
