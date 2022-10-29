from django.shortcuts import render
from django.core.management import call_command
from blog.forms import ArticleForm
from blog.models import Article
from markata import Markata

def archives(request):
    #markata = Markata()
    #articles = markata.articles
    #for article in articles:
    #    article_obj = Article.objects.filter(title=article["title"])
    #    if article_obj:
    #        article["edit_link"] += f"{article_obj[0].id}/change"
    return render(request, "markout/archive/index.html")

def build(request):
    call_command("build")
    return render(request, "markout/archive/index.html")

def createArticle(request):
    form = ArticleForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            article = form.save()
            build(request)
            return render(request, 'markout/archive/index.html')
    context = {
        'form': form,
    }
    return render(request, 'templates/blog/add.html', context)
