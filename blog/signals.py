from django.db.models.signals import pre_save
from django.dispatch import receiver
from pathlib import Path
from blog.models import Article 

from markata import Markata, __version__

@receiver(pre_save, sender=Article)
def call_markata(sender, instance, **kwargs):
    markata = Markata()
    print(markata.config.keys())
    print(instance.__dict__)
    md_frontmatter = f"""---
templateKey: {instance.template_key} 
title: {instance.title}
status: {instance.status}
---
    """
    post_archive = markata.config.get("glob_patterns")
    with open(Path("pages") / f"{instance.title}.md", 'w', encoding="utf-8") as f:
        f.write(md_frontmatter)
        f.write(instance.content)
