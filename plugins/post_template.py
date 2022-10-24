import copy
from pathlib import Path, PosixPath
from typing import TYPE_CHECKING

import jinja2
from deepmerge import always_merger
from jinja2 import Template, Undefined, Environment, FileSystemLoader
from more_itertools import flatten

from markata import __version__
from markata.hookspec import hook_impl

env = jinja2.Environment()

if TYPE_CHECKING:
    from markata import Markata


class SilentUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return ""


@hook_impl
def configure(markata: "Markata") -> None:
    """
    Massages the configuration limitations of toml to allow a little bit easier
    experience to the end user making configurations while allowing an simpler
    jinja template.  This enablees the use of the `markata.head.text` list in
    configuration.
    """

    raw_text = markata.config.get("head", {}).get("text", "")

    if isinstance(raw_text, list):
        markata.config["head"]["text"] = "\n".join(
            flatten([t.values() for t in raw_text])
        )


@hook_impl
def pre_render(markata: "Markata") -> None:
    """
    FOR EACH POST: Massages the configuration limitations of toml/yaml to allow
    a little bit easier experience to the end user making configurations while
    allowing an simpler jinja template.  This enablees the use of the
    `markata.head.text` list in configuration.
    """
    for article in [a for a in markata.articles if "config_overrides" in a.keys()]:
        raw_text = article.get("config_overrides", {}).get("head", {}).get("text", "")

        if isinstance(raw_text, list):
            article["config_overrides"]["head"]["text"] = "\n".join(
                flatten([t.values() for t in raw_text])
            )


@hook_impl
def render(markata: "Markata") -> None:
    if "post_template" in markata.config:
        template_file = markata.config["post_template"]
    else:
        template_file = Path(__file__).parent / "default_post_template.html"
    with open(template_file) as f:
        env = Environment()
        templates_dir = str(Path(template_file).parent.parent)
        
        env.loader = FileSystemLoader(searchpath=templates_dir)
        if type(template_file) is PosixPath and template_file in env.list_templates():
            template_file = env.get_template(template_file.name)
        #else:
        #    template = Template(f.read())
        template = env.get_template(template_file)
        #template = Template(f.read(), undefined=SilentUndefined)

    if "{{" in str(markata.config.get("head", {})):
        head_template = Template(
            str(markata.config.get("head", {})), undefined=SilentUndefined
        )
    else:
        head_template = None
        head = {}

    _full_config = copy.deepcopy(markata.config)

    for article in [a for a in markata.articles if hasattr(a, "html")]:

        if head_template:

            head = eval(
                head_template.render(
                    __version__=__version__,
                    config=_full_config,
                    **article,
                )
            )

        merged_config = {
            **_full_config,
            **{"head": head},
        }

        merged_config = always_merger.merge(
            merged_config,
            copy.deepcopy(
                article.get(
                    "config_overrides",
                    {},
                )
            ),
        )

        article.html = template.render(
            __version__=__version__,
            body=article.html,
            toc=markata.md.toc,  # type: ignore
            config=merged_config,
            **article.metadata,
        )
