#!/usr/bin/env python3
"""Scan repo for HTML pages and regenerate index.html."""

import os
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
EXCLUDE = {"index.html"}


def extract_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else path.stem


def find_pages():
    pages = []
    for f in sorted(ROOT.rglob("*.html")):
        rel = f.relative_to(ROOT)
        parts = rel.parts
        # skip hidden dirs, node_modules, and excluded files
        if any(p.startswith(".") or p == "node_modules" for p in parts):
            continue
        if rel.name in EXCLUDE:
            continue
        pages.append((str(rel).replace("\\", "/"), extract_title(f)))
    return pages


def render(pages):
    if not pages:
        cards = '<p style="color:var(--ink-faint);text-align:center;padding:3rem 0;">尚無頁面</p>'
    else:
        items = []
        for href, title in pages:
            items.append(f"""
      <a class="card" href="{href}">
        <span class="card-title">{title}</span>
        <span class="card-href">{href}</span>
        <span class="card-arrow">→</span>
      </a>""")
        cards = "\n".join(items)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>行程總覽</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Noto+Serif+TC:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --sand: #F5EFE0; --sand-dark: #E8DFC8;
    --ink: #1A1410; --ink-muted: #5C4F3D; --ink-faint: #9C8E7A;
    --aegean: #1B4F72; --gold: #C9A84C; --white: #FDFAF4;
  }}
  body {{ font-family: 'Noto Serif TC', serif; background: var(--sand); color: var(--ink); min-height: 100vh; }}

  header {{
    background: var(--aegean);
    padding: 4rem 3rem 3rem;
  }}
  .header-tag {{
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    color: var(--gold);
    margin-bottom: 1rem;
  }}
  header h1 {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 400;
    color: #fff;
    line-height: 1.1;
  }}
  header h1 em {{ font-style: italic; color: #A8D8EA; }}

  main {{
    max-width: 760px;
    margin: 0 auto;
    padding: 3rem;
  }}
  .list-label {{
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    color: var(--ink-faint);
    margin-bottom: 1.2rem;
  }}
  .card {{
    display: flex;
    align-items: center;
    gap: 1rem;
    background: var(--white);
    border: 0.5px solid var(--sand-dark);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.75rem;
    text-decoration: none;
    transition: border-color 0.2s, box-shadow 0.2s;
  }}
  .card:hover {{
    border-color: var(--gold);
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  }}
  .card-title {{
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    color: var(--ink);
    flex: 1;
  }}
  .card-href {{
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: var(--ink-faint);
    letter-spacing: 0.05em;
  }}
  .card-arrow {{
    color: var(--gold);
    font-size: 1rem;
    flex-shrink: 0;
  }}

  footer {{
    border-top: 0.5px solid var(--sand-dark);
    padding: 1.5rem 3rem;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: var(--ink-faint);
    letter-spacing: 0.12em;
    max-width: 760px;
    margin: 0 auto;
  }}

  @media (max-width: 640px) {{
    header {{ padding: 3rem 1.5rem 2rem; }}
    main {{ padding: 2rem 1.5rem; }}
    footer {{ padding: 1.5rem; }}
    .card-href {{ display: none; }}
  }}
</style>
</head>
<body>

<header>
  <div class="header-tag">TRIP PAGES · 行程頁面</div>
  <h1>行程<br><em>總覽</em></h1>
</header>

<main>
  <div class="list-label">ALL PAGES · 共 {len(pages)} 頁</div>
  {cards}
</main>

<footer>AUTO-GENERATED · 每次新增頁面後自動更新</footer>

</body>
</html>
"""


if __name__ == "__main__":
    pages = find_pages()
    html = render(pages)
    out = ROOT / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"Generated index.html with {len(pages)} page(s):")
    for href, title in pages:
        print(f"  {href}  —  {title}")
