from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import app

DIST = ROOT / "dist"
STATIC_SRC = ROOT / "templates" / "static"
STATIC_DEST = DIST / "static"


def main():
    if DIST.exists():
        shutil.rmtree(DIST)

    DIST.mkdir(parents=True)
    shutil.copytree(STATIC_SRC, STATIC_DEST)

    with app.test_client() as client:
        response = client.get("/")
        if response.status_code >= 400:
            raise RuntimeError(f"Failed to render /: {response.status_code}")
        html = response.get_data(as_text=True)

    # GitHub Pages project sites live under /repo-name/, so root-relative
    # Flask static URLs like /static/... must become relative static/... URLs.
    html = html.replace('"/static/', '"static/')
    html = html.replace("'/static/", "'static/")

    (DIST / "index.html").write_text(html, encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built static site at {DIST}")


if __name__ == "__main__":
    main()
