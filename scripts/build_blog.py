"""Build the blog: blog/posts/*.md -> blog/<slug>/index.html, blog/index.html, sitemap.xml.

Run:  python scripts/build_blog.py
No packages needed. The posts use a small part of Markdown: ## headings, paragraphs,
- and 1. lists, ``` code blocks, **bold**, *italic*, `code` and [links](url).
"""

import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "blog", "posts")
SITE = "https://edittools.szy.monster"
DATE = "2026-11-09"
DATE_TEXT = "9 November 2026"


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", text)

    def link(m):
        label, url = m.group(1), m.group(2)
        ext = url.startswith("http")
        attrs = ' target="_blank" rel="noopener"' if ext else ""
        return f'<a href="{url}"{attrs}>{label}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)


def markdown(src):
    out, para, lst, code = [], [], None, None

    def flush():
        nonlocal para, lst
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []
        if lst:
            tag, items = lst
            out.append(f"<{tag}>" + "".join(f"<li>{inline(i)}</li>" for i in items) + f"</{tag}>")
            lst = None

    for line in src.splitlines():
        if code is not None:
            if line.startswith("```"):
                out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
                code = None
            else:
                code.append(line)
            continue
        if line.startswith("```"):
            flush()
            code = []
        elif line.startswith("## "):
            flush()
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif re.match(r"^\s*[-*] ", line):
            if para or (lst and lst[0] != "ul"):
                flush()
            lst = lst or ("ul", [])
            lst[1].append(re.sub(r"^\s*[-*] ", "", line))
        elif re.match(r"^\s*\d+\. ", line):
            if para or (lst and lst[0] != "ol"):
                flush()
            lst = lst or ("ol", [])
            lst[1].append(re.sub(r"^\s*\d+\. ", "", line))
        elif not line.strip():
            flush()
        elif lst and line.startswith("  "):
            lst[1][-1] += " " + line.strip()
        else:
            if lst:
                flush()
            para.append(line.strip())
    flush()
    return "\n".join(out)


def read_post(path):
    raw = open(path, encoding="utf-8").read()
    _, front, body = raw.split("---", 2)
    meta = {}
    for line in front.strip().splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    meta["slug"] = os.path.splitext(os.path.basename(path))[0]
    meta["order"] = int(meta.get("order", 99))
    meta["body"] = markdown(body.strip())
    return meta


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="AutoSubtitler">
  <meta name="color-scheme" content="dark">
  <link rel="stylesheet" href="/style.css">
  {jsonld}
</head>
<body>
  <main class="wrap">
    <header class="top">
      <a class="home" href="/"><h1>AutoSubtitler</h1></a>
      <span class="by"><a href="/blog/">Blog</a></span>
      <a class="btn btn-primary right" href="/">Make subtitles free</a>
    </header>
{content}
    <footer class="foot">
      <a href="/">AutoSubtitler</a>
      <a href="/blog/">Blog</a>
      <a href="/privacy.html">Privacy</a>
      <a href="https://github.com/SzymonDevGit/editingTools" target="_blank" rel="noopener">Source on GitHub</a>
      <a href="https://discord.gg/bHxaXgjpfe" target="_blank" rel="noopener">Bugs &amp; suggestions</a>
    </footer>
  </main>
</body>
</html>
"""

CTA = """    <aside class="cta">
      <b>Make the .srt for free</b>
      <span>Whisper subtitles in your browser. No sign-up, no upload, no watermark.</span>
      <a class="btn btn-primary" href="/">Open AutoSubtitler</a>
    </aside>"""


def esc(s):
    return html.escape(s, quote=True)


def jsonld(obj):
    import json
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def main():
    posts = sorted((read_post(os.path.join(POSTS, f)) for f in os.listdir(POSTS) if f.endswith(".md")),
                   key=lambda p: p["order"])
    for p in posts:
        url = f"{SITE}/blog/{p['slug']}/"
        related = [o for o in posts if o is not p and (("editor" in o) != ("editor" in p))][:3]
        rel = "".join(f'<li><a href="/blog/{o["slug"]}/">{esc(o["title"])}</a></li>' for o in related)
        content = f"""    <article class="post md">
      <p class="crumbs"><a href="/blog/">Blog</a> › {esc(p.get('editor', 'Guide'))}</p>
      <h1 class="post-title">{esc(p['title'])}</h1>
      <p class="muted small">Updated {DATE_TEXT} · by Szymon at szy.monster</p>
{p['body']}
    </article>
{CTA}
    <nav class="related"><h2>Related</h2><ul>{rel}</ul></nav>"""
        ld = jsonld({
            "@context": "https://schema.org", "@type": "Article",
            "headline": p["title"], "description": p["description"],
            "datePublished": DATE, "dateModified": DATE,
            "author": {"@type": "Person", "name": "Szymon"},
            "publisher": {"@type": "Organization", "name": "szy.monster", "url": "https://szy.monster/"},
            "mainEntityOfPage": url,
        })
        out = os.path.join(ROOT, "blog", p["slug"])
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
            f.write(PAGE.format(title=esc(p["title"]), desc=esc(p["description"]), url=url,
                                og_type="article", jsonld=ld, content=content))

    guides = [p for p in posts if "editor" not in p]
    editors = [p for p in posts if "editor" in p]
    card = lambda p: (f'<li><a href="/blog/{p["slug"]}/"><b>{esc(p["title"])}</b>'
                      f'<span>{esc(p["description"])}</span></a></li>')
    content = f"""    <section class="md blog-index">
      <h1 class="post-title">Free subtitling for video: guides</h1>
      <p class="muted">How to make subtitles for free with Whisper, and how to add them to your editor or YouTube.</p>
      <h2>Start here</h2>
      <ul class="cards">{''.join(card(p) for p in guides)}</ul>
      <h2>By editor</h2>
      <ul class="cards">{''.join(card(p) for p in editors)}</ul>
    </section>
{CTA}"""
    with open(os.path.join(ROOT, "blog", "index.html"), "w", encoding="utf-8") as f:
        f.write(PAGE.format(title="Free subtitling for video: guides · AutoSubtitler",
                            desc="Guides to free video subtitles with Whisper: make an SRT file and add it to DaVinci Resolve, Premiere Pro, Final Cut Pro, CapCut, YouTube and more.",
                            url=f"{SITE}/blog/", og_type="website", jsonld="", content=content))

    urls = [f"{SITE}/", f"{SITE}/blog/"] + [f"{SITE}/blog/{p['slug']}/" for p in posts] + [f"{SITE}/privacy.html"]
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"  <url><loc>{u}</loc><lastmod>{DATE}</lastmod></url>\n")
        f.write("</urlset>\n")
    print(f"Built {len(posts)} posts")


if __name__ == "__main__":
    main()
