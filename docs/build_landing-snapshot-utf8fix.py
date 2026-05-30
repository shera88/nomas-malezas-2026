"""Build dist/index.wp.html from src/index.html: minify + inject SEO + JSON-LD."""
import subprocess
import os
import re
import json
from pathlib import Path

ROOT = Path(r"D:\Claude\No más malezas")
SRC = ROOT / "src" / "index.html"
DIST = ROOT / "dist"
OUT = DIST / "index.wp.html"
DIST.mkdir(exist_ok=True)

src = SRC.read_text(encoding="utf-8")

# Extract style block + body content (inside <article>/page)
m_style_start = src.find("<style>")
m_body_end = src.rfind("</body>")
m_div_open = src.find('<div class="nmm-2026">')
style_end = src.find("</style>", m_style_start) + len("</style>")

style_block = src[m_style_start:style_end]
body_block = src[m_div_open:m_body_end].rstrip()

# JSON-LD Event schema (added to <head> via meta-injection — for WP page we put inside content prepended)
EVENT_LD = {
    "@context": "https://schema.org",
    "@type": "Event",
    "name": "7° Congreso Internacional No Más Malezas 2026",
    "description": "1 de junio de 2026 · FEXPOCRUZ Salón Guarayos. 4 disertantes internacionales en barbecho, pre-emergentes y malezas resistentes. Inscripción gratuita.",
    "startDate": "2026-06-01T14:00:00-04:00",
    "endDate": "2026-06-01T20:00:00-04:00",
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "location": {
        "@type": "Place",
        "name": "FEXPOCRUZ — Salón Guarayos",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Santa Cruz de la Sierra",
            "addressCountry": "BO"
        }
    },
    "image": [
        "https://cdn.jsdelivr.net/gh/shera88/nomas-malezas-2026@main/Ilustrator/Logo%20Ok/b/1x/Recurso%2015.png"
    ],
    "organizer": {
        "@type": "Organization",
        "name": "MAINTER",
        "url": "https://www.mainter.com.bo"
    },
    "performer": [
        {"@type": "Person", "name": "Dr. Pedro Christoffoleti", "nationality": "BR"},
        {"@type": "Person", "name": "Ing. Lucas Paterlini", "nationality": "AR"},
        {"@type": "Person", "name": "Ing. Agro. Alexandre Camilo", "nationality": "BR"},
        {"@type": "Person", "name": "Ing. Agr. M.Sc. Pablo Franco", "nationality": "BO"}
    ],
    "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "BOB",
        "availability": "https://schema.org/InStock",
        "url": "https://www.mainter.com.bo/no-mas-malezas-2026/#registro"
    },
    "inLanguage": "es",
    "isAccessibleForFree": True
}

ld_block = (
    '<script type="application/ld+json">'
    + json.dumps(EVENT_LD, ensure_ascii=False, separators=(",", ":"))
    + "</script>"
)

# SEO meta block (these go at top of content; WP <head> already has title meta but we add OG-style)
seo_block = """<meta name="description" content="1 de junio de 2026 · FEXPOCRUZ Salón Guarayos. 4 disertantes internacionales en barbecho, pre-emergentes y malezas resistentes. Inscripción gratuita.">
<meta property="og:title" content="7° Congreso Internacional No Más Malezas 2026">
<meta property="og:description" content="1 de junio · Santa Cruz, Bolivia. Disertantes de Brasil, Argentina y Bolivia. Inscripción gratuita.">
<meta property="og:image" content="https://cdn.jsdelivr.net/gh/shera88/nomas-malezas-2026@main/Ilustrator/Logo%20Ok/b/1x/Recurso%2015.png">
<meta property="og:url" content="https://www.mainter.com.bo/no-mas-malezas-2026/">
<meta property="og:type" content="event">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://www.mainter.com.bo/no-mas-malezas-2026/">"""

# Assemble pre-min content (WP page content blob)
content_raw = seo_block + "\n" + ld_block + "\n" + style_block + "\n" + body_block

# Write tmp uncompressed
tmp = DIST / "_tmp_pre.html"
tmp.write_text(content_raw, encoding="utf-8")

# Minify via html-minifier-terser
minified = DIST / "_tmp_min.html"
cmd = [
    "html-minifier-terser.cmd" if os.name == "nt" else "html-minifier-terser",
    str(tmp),
    "-o", str(minified),
    "--collapse-whitespace",
    "--remove-comments",
    "--minify-css", "true",
    "--minify-js", '{"compress":{"drop_console":false,"passes":2},"mangle":true}',
    "--remove-redundant-attributes",
    "--remove-script-type-attributes",
    "--remove-style-link-type-attributes",
    "--use-short-doctype",
    "--decode-entities",
]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("MINIFY ERROR:", r.stderr[:1000])
    raise SystemExit(1)

out_html = minified.read_text(encoding="utf-8")

# WP `convert_chars` filter rewrites && → &#038;&#038; inside any text node — including <script> bodies.
# Wrap each inline <script> body in base64 so the source bytes never touch the filter.
import base64
import re

def wrap_script(m):
    attrs = m.group(1) or ""
    body = m.group(2)
    # Skip if has src, or is JSON-LD/application/ld+json/template
    if re.search(r'\bsrc\s*=', attrs):
        return m.group(0)
    if re.search(r'\btype\s*=\s*["\']application/(ld\+json|json)["\']', attrs):
        return m.group(0)
    if re.search(r'\btype\s*=\s*["\'](text/template|text/x-template)["\']', attrs):
        return m.group(0)
    body = body.strip()
    if not body:
        return m.group(0)
    b64 = base64.b64encode(body.encode("utf-8")).decode("ascii")
    # Use TextDecoder for proper UTF-8 decoding (atob alone treats bytes as Latin-1, mangles tildes/ñ)
    return f'<script>(new Function(new TextDecoder().decode(Uint8Array.from(atob("{b64}"),c=>c.charCodeAt(0)))))()</script>'

wrapped = re.sub(
    r'<script([^>]*)>([\s\S]*?)</script>',
    wrap_script,
    out_html,
)

OUT.write_text(wrapped, encoding="utf-8")
print(f"raw:      {len(content_raw):,} chars")
print(f"minified: {len(out_html):,} chars  ({100*len(out_html)/len(content_raw):.0f}%)")
print(f"b64-wrap: {len(wrapped):,} chars  ({100*len(wrapped)/len(content_raw):.0f}%)")
print(f"saved:    {OUT}")

# Cleanup
tmp.unlink()
minified.unlink()
