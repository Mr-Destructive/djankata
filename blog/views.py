from django.shortcuts import render
from django.core.management import call_command
from blog.models import Article
from markata import Markata

def archives(request):
    markata = Markata()
    articles = markata.articles
    call_command("build")
    for article in articles:
        article_obj = Article.objects.filter(title=article["title"])
        if article_obj:
            article["edit_link"] += f"{article_obj[0].id}/change"
    return render(request, "archive/index.html")
