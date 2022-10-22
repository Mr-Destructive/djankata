from pathlib import Path
from typing import TYPE_CHECKING

from markata.hookspec import hook_impl

if TYPE_CHECKING:
    from markata import Markata


def _is_relative_to(output_dir: Path, output_html: Path):
    try:
        output_html.relative_to(output_dir)
        return True
    except ValueError:
        return False


@hook_impl
def pre_render(markata: "Markata") -> None:
    """
    Sets the `output_html` in the articles metadata.  If the output is
    explicitly given, it will make sure its in the `output_dir`, if it is not
    explicitly set it will use the articles slug.
    """
    output_dir = Path(markata.config["output_dir"])  # type: ignore
    output_dir.mkdir(parents=True, exist_ok=True)

    for article in markata.articles:
        if "output_html" in article.metadata:
            article_path = Path(article["output_html"])
            if not _is_relative_to(output_dir, article_path):
                article["output_html"] = output_dir / article["output_html"]
        elif article["slug"] == "index":
            article["output_html"] = output_dir / "index.html"
        else:
            article["output_html"] = output_dir / article["slug"] 
        print(article["output_html"])


@hook_impl
def save(markata: "Markata") -> None:
    """
    Saves all the articles to their set `output_html` location if that location
    is relative to the specified `output_dir`.  If its not relative to the
    `output_dir` it will log an error and move on.
    """
    output_dir = Path(markata.config["output_dir"])  # type: ignore

    for article in markata.articles:
        article_path = Path(article["output_html"])
        if _is_relative_to(output_dir, article_path):
            article_path.parent.mkdir(parents=True, exist_ok=True)
            with open(article_path, "w+") as f:
                f.write(article.html)
        else:
            markata.console.log(
                f'article "{article["path"]}" attempted to write to "{article["output_html"]}" outside of the configured output_dir "{output_dir}"'
            )
