from pathlib import Path
from typing import TYPE_CHECKING

from slugify import slugify

from markata.hookspec import hook_impl

if TYPE_CHECKING:
    from markata import Markata


@hook_impl(tryfirst=True)
def pre_render(markata: "Markata") -> None:
    """
    Sets the article slug if one is not already set in the frontmatter.
    """
    should_slugify = markata.config.get("slugify", True)
    for article in markata.iter_articles(description="creating slugs"):
        stem = article.get(
            "slug", Path(article.get("path", article.get("title", ""))).stem
        )
        if should_slugify:
            article["slug"] = "/".join([slugify(s) for s in stem.split("/")])
        else:
            article["slug"] = stem

        article["slug"] += "/index.html"
