import frontmatter
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from pathlib import Path
from blog.models import Article 
from django.shortcuts import redirect

from markata import Markata, __version__

@receiver(post_save, sender=Article)
def call_markata(sender, instance, **kwargs):
    markata = Markata()
    md_frontmatter = f"""---
templateKey: {instance.template_key} 
title: {instance.title}
status: {instance.status}
---
    """
    #instance.edit_link = "/admin/blog/article/" + instance.id + "/change"
    #instance.save()
    title_path = instance.title.replace(" ", "_")
    with open(Path("blog/pages") / f"{title_path}.md", 'w', encoding="utf-8") as f:
        f.write(md_frontmatter)
        f.write(instance.content)

    articles = markata.articles
    article = list(filter(lambda d: d['title'] == "test", articles))[0]
    article["edit_link"] = f"/admin/blog/article/{instance.id}/change"

    return redirect("archive")

def write_markdown_post(article):
    post = frontmatter.loads(article)
    title_path = post.get('title').replace(" ", "_")
    with open(Path("blog/pages") / f"{title_path}.md", 'w', encoding="utf-8") as f:
        f.write(article)

