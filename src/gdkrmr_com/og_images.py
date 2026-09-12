"""Pre-render hook: fill in missing project images from Open Graph metadata.

For every post in software/posts/ that has a `link:` in its front matter but
no `image:` (or an `image:` pointing to a file that does not exist), fetch the
linked page, read its og:image, download the image to software/posts/images/
and set the `image:` entry in the post's front matter.

Images already on disk are not re-downloaded, so the network is only hit for
new posts (or after deleting a cached image).
"""

import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup

POSTS_DIR = Path("software/posts")
IMAGES_DIR = POSTS_DIR / "images"

EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
}

FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def split_front_matter(text):
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return None, None
    return yaml.safe_load(m.group(1)), m


def find_cached_image(stem):
    if not IMAGES_DIR.is_dir():
        return None
    for path in IMAGES_DIR.iterdir():
        if path.stem == stem:
            return path
    return None


def fetch_og_image_url(link):
    resp = requests.get(link, timeout=15, headers={"User-Agent": "gdkrmr.com build"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    tag = soup.find("meta", property="og:image") or soup.find(
        "meta", attrs={"name": "twitter:image"}
    )
    if tag is None or not tag.get("content"):
        return None
    return urljoin(link, tag["content"])


def download_image(url, stem):
    resp = requests.get(url, timeout=30, headers={"User-Agent": "gdkrmr.com build"})
    resp.raise_for_status()
    content_type = resp.headers.get("content-type", "").split(";")[0].strip()
    ext = EXTENSIONS.get(content_type) or Path(urlparse(url).path).suffix or ".png"
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    path = IMAGES_DIR / f"{stem}{ext}"
    path.write_bytes(resp.content)
    return path


IMAGE_LINE_RE = re.compile(r"^image:.*$", re.MULTILINE)


def set_front_matter_image(qmd_path, text, match, image_path):
    rel = image_path.relative_to(POSTS_DIR).as_posix()
    line = f'image: "{rel}"'
    front = match.group(1)
    if IMAGE_LINE_RE.search(front):
        new_front = IMAGE_LINE_RE.sub(line, front, count=1)
        new_text = text[: match.start(1)] + new_front + text[match.end(1) :]
    else:
        end = match.end(1)  # insert just before the closing ---
        new_text = text[:end] + "\n" + line + text[end:]
    qmd_path.write_text(new_text)


def process(qmd_path):
    text = qmd_path.read_text()
    meta, match = split_front_matter(text)
    if not isinstance(meta, dict):
        return
    declared = meta.get("image")
    if declared and (qmd_path.parent / declared).is_file():
        return
    link = meta.get("link")

    cached = find_cached_image(qmd_path.stem)
    if cached is None:
        if not link:
            return
        print(f"og_images: fetching og:image for {qmd_path.name} from {link}")
        og_url = fetch_og_image_url(link)
        if og_url is None:
            print(f"og_images: no og:image found at {link}", file=sys.stderr)
            return
        cached = download_image(og_url, qmd_path.stem)
        print(f"og_images: saved {cached}")

    if declared != cached.relative_to(POSTS_DIR).as_posix():
        set_front_matter_image(qmd_path, text, match, cached)
        print(f"og_images: set image for {qmd_path.name} -> {cached.name}")


def main():
    for qmd_path in sorted(POSTS_DIR.glob("*.qmd")):
        try:
            process(qmd_path)
        except requests.RequestException as exc:
            print(f"og_images: failed for {qmd_path.name}: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
