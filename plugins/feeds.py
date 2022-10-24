import datetime
import shutil
import textwrap
from pathlib import Path, PosixPath
from typing import TYPE_CHECKING, Any, List, Optional, Union

from jinja2 import Template, Undefined, Environment, FileSystemLoader

from markata import Markata, __version__
from markata.hookspec import hook_impl

if TYPE_CHECKING:
    from frontmatter import Post


class SilentUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return ""


class MarkataFilterError(RuntimeError):
    ...


@hook_impl
def configure(markata: Markata) -> None:
    """
    configure the default values for the feeds plugin
    """
    if "feeds" not in markata.config.keys():
        markata.config["feeds"] = dict()
    config = markata.config.get("feeds", dict())
    if "archive" not in config.keys():
        config["archive"] = dict()
        config["archive"]["filter"] = "True"

    default_post_template = config.get(
        "template", Path(__file__).parent / "default_post_template.html"
    )
    for page, page_conf in config.items():
        if "template" not in page_conf.keys():
            page_conf["template"] = default_post_template


@hook_impl
def save(markata: Markata) -> None:
    """
    Creates a new feed page for each page in the config.
    """
    feeds = markata.config.get("feeds", {})

    description = markata.get_config("description") or ""
    url = markata.get_config("url") or ""

    for page, page_conf in feeds.items():

        create_page(
            markata,
            page,
            description=description,
            url=url,
            **page_conf,
        )

    home = Path(str(markata.config["output_dir"])) / "index.html"
    archive = Path(str(markata.config["output_dir"])) / "archive" / "index.html"
    if not home.exists() and archive.exists():
        shutil.copy(str(archive), str(home))


def create_page(
    markata: Markata,
    page: str,
    tags: Optional[List] = None,
    status: str = "published",
    template: Optional[Union[Path, str]] = None,
    card_template: Optional[str] = None,
    filter: Optional[str] = None,
    description: Optional[str] = None,
    url: Optional[str] = None,
    title: Optional[str] = "feed",
    sort: str = "True",
    reverse: bool = False,
    **rest,
) -> None:
    """
    create an html unorderd list of posts.
    """

    posts = markata.map("post", filter=filter, sort=sort, reverse=reverse)
    # if filter is not None:
    #     posts = reversed(
    #         sorted(
    #             markata.articles, key=lambda x: x.get("date", datetime.date(1970, 1, 1))
    #         )
    #     )
    #     try:
    #         posts = [post for post in posts if eval(filter, post.to_dict(), {})]
    #     except Exception as e:
    #         msg = textwrap.dedent(
    #             f"""
    #                 While processing feed page='{page}' markata hit the following exception
    #                 during filter='{filter}'
    #                 {e}
    #                 """
    #         )
    #         raise MarkataFilterError(msg)

    cards = [create_card(post, card_template) for post in posts]
    cards.insert(0, "<ul>")
    cards.append("</ul>")

    with open(template) as f:
        env = Environment()
        templates_dir = markata.config.get("templates_dir")
        templates_dir = str(Path(template).parent.parent) if not templates_dir else templates_dir[title] 
        
        env.loader = FileSystemLoader(searchpath=templates_dir)
        if type(template) is PosixPath and template in env.list_templates():
            template = env.get_template(template.name)
        #else:
        #    template = Template(f.read())
        template = env.get_template(template)

    output_file = Path(markata.config["output_dir"]) / page / "index.html"
    canonical_url = f"{url}/{page}/"
    output_file.parent.mkdir(exist_ok=True, parents=True)

    with open(output_file, "w+") as f:
        f.write(
            template.render(
                __version__=__version__,
                body="".join(cards),
                url=url,
                description=description,
                title=title,
                canonical_url=canonical_url,
                today=datetime.datetime.today(),
                config=markata.config,
            )
        )


def create_card(post: "Post", template: Optional[str] = None) -> Any:
    """
    Creates a card for one post based on the configured template.  If no
    template is configured it will create one with the post title and dates (if present).
    """
    if template is None:
        if "date" in post.keys():
            return textwrap.dedent(
                f"""
                <li class='post'>
                <a href="/{post['slug']}/">
                    {post['title']} {post['date'].year}-{post['date'].month}-{post['date'].day}
                </a>
                </li>
                """
            )
        else:
            return textwrap.dedent(
                f"""
                <li class='post'>
                <a href="/{post['slug']}/">
                    {post['title']}
                </a>
                </li>
                """
            )
    try:
        _template = Template(Path(template).read_text())
    except FileNotFoundError:
        _template = Template(template)
    return _template.render(**post.to_dict())
