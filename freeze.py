"""
Generate a fully static version of the site.

    python freeze.py

Output goes to  _static/
Deploy that folder to GitHub Pages, Netlify, or any static host.

── GitHub Pages notes ───────────────────────────────────────────────
If hosting at  https://username.github.io/repo-name/
set the env var FREEZER_BASE_URL before running:

    set FREEZER_BASE_URL=https://username.github.io/repo-name/
    python freeze.py

For a custom domain (e.g. https://www.yourdomain.com/) leave it unset.
─────────────────────────────────────────────────────────────────────
"""
import os
import shutil

# Must import app AFTER any env vars are set
from app import app, create_tables

# Tell the site template to use Formspree/mailto instead of Flask form handler
app.config["STATIC_MODE"] = True

# Allow overriding base URL for subdirectory deployments
base_url = os.environ.get("FREEZER_BASE_URL", "")
if base_url:
    app.config["FREEZER_BASE_URL"] = base_url

import warnings
from flask_frozen import Freezer, MissingURLGeneratorWarning

# with_no_argument_rules=False stops Frozen-Flask auto-discovering admin routes
freezer = Freezer(app, with_static_files=True, with_no_argument_rules=False, log_url_for=False)


@freezer.register_generator
def index():
    """Only freeze the public homepage."""
    yield {}


if __name__ == "__main__":
    create_tables()

    out = app.config.get("FREEZER_DESTINATION", "_static")
    print(f"Building static site -> {out}/")

    with app.app_context():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", MissingURLGeneratorWarning)
            freezer.freeze()

    print(f"Done! Static site is in {out}/")
    print()
    print("To deploy to GitHub Pages:")
    print(f"  1. Copy the contents of {out}/ to your gh-pages branch")
    print("  2. Or use: gh-pages -d _static (if you have the npm tool)")
    print()
    print("To deploy to Netlify:")
    print("  Drag and drop the _static/ folder at app.netlify.com/drop")
