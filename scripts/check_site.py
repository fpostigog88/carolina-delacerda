#!/usr/bin/env python3
"""Validate site links, SEO metadata, structured data, and sitemap without third-party deps."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "carolinadelacerda.com"
errors = []

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.meta = {}
        self.canonicals = []
        self.schemas = []
        self.title = 0
        self.h1 = 0
        self.main = 0
        self.json_mode = False
        self.buf = ""

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag in ("title", "h1", "main"):
            setattr(self, tag, getattr(self, tag) + 1)
        if tag == "meta":
            self.meta[attrs.get("name") or attrs.get("property")] = attrs.get("content")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href"))
        if tag in ("a", "img", "link", "script"):
            for attr in ("href", "src"):
                if attrs.get(attr):
                    self.links.append((attr, attrs[attr]))
        if tag == "img" and not attrs.get("alt"):
            errors.append("Missing image alt attribute")
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.json_mode = True
            self.buf = ""

    def handle_data(self, data):
        if self.json_mode:
            self.buf += data

    def handle_endtag(self, tag):
        if tag == "script" and self.json_mode:
            self.schemas.append(self.buf)
            self.json_mode = False

def resolve(page, link):
    url = urlsplit(link)
    if url.scheme not in ("", "http", "https"):
        return None
    if url.netloc and url.hostname != DOMAIN:
        return None
    if url.netloc or url.scheme:
        target = ROOT / unquote(url.path).lstrip("/")
    else:
        target = page.parent / unquote(url.path)
    try:
        target = target.resolve()
        target.relative_to(ROOT)
    except ValueError:
        errors.append(f"{page}: link escapes root: {link}")
        return None
    if target.is_dir() or not target.suffix:
        target = target / "index.html"
    return target, unquote(url.fragment)

pages = {}
for file in sorted(ROOT.rglob("*.html")):
    # GitHub Pages serves 404.html as a real HTTP 404; it must not be indexed.
    is_not_found = file.name == "404.html"
    doc = Page()
    doc.feed(file.read_text(encoding="utf-8"))
    pages[file.resolve()] = doc
    label = str(file.relative_to(ROOT))
    if (doc.title, doc.h1, doc.main) != (1, 1, 1):
        errors.append(f"{label}: expected one each of title, h1, main")
    if not is_not_found and (not doc.meta.get("description") or not doc.meta.get("og:image")):
        errors.append(f"{label}: missing description or sharing image")
    if not is_not_found and len(doc.canonicals) != 1:
        errors.append(f"{label}: missing or duplicate canonical")
    if not is_not_found and len(doc.schemas) != 1:
        errors.append(f"{label}: missing or duplicate schema JSON-LD")
    if is_not_found and doc.meta.get("robots") != "noindex, follow":
        errors.append("404.html: must not be indexed")
    for src in doc.schemas:
        try:
            schema = json.loads(src)
            types = {n.get("@type") for n in schema.get("@graph", [])}
            if not {"Person", "WebSite"}.issubset(types):
                errors.append(f"{label}: missing Person or WebSite markup")
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: invalid JSON-LD: {exc}")

for file, doc in pages.items():
    for attr, url in doc.links:
        found = resolve(file, url)
        if found is None:
            continue
        target, anchor = found
        if not target.is_file():
            errors.append(f"{file.relative_to(ROOT)}: broken {attr}={url}")
        elif anchor and target in pages and anchor not in pages[target].ids:
            errors.append(f"{file.relative_to(ROOT)}: missing anchor in {url}")

try:
    tree = ElementTree.parse(ROOT / "sitemap.xml")
    urls = [n.text.strip() for n in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    expected = {"https://" + DOMAIN + "/" + ("" if page == ROOT / "index.html" else page.parent.relative_to(ROOT).as_posix() + "/") for page in pages if page.name != "404.html"}
    if len(urls) != len(set(urls)) or set(urls) != expected:
        errors.append(f"Sitemap mismatch: missing {expected-set(urls)}, extra {set(urls)-expected}")
except (OSError, ElementTree.ParseError) as exc:
    errors.append(f"Invalid sitemap: {exc}")
if "Allow: /" not in (ROOT / "robots.txt").read_text(encoding="utf-8"):
    errors.append("Robots file missing allow rule")
if (ROOT / "CNAME").read_text(encoding="utf-8").strip() != DOMAIN:
    errors.append("CNAME mismatch")

for err in errors:
    print("FAIL:", err)
print(f"{'FAIL' if errors else 'PASS'}: {len(pages)} pages, {sum(len(p.links) for p in pages.values())} links, schema and sitemap, {len(errors)} errors")
sys.exit(bool(errors))
