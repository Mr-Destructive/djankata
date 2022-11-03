from django.shortcuts import render
from django.core.management import call_command
from blog.forms import ArticleForm, CustomFeedsForm
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


def customFeedGenerator(feed_name, feed_filter):
    feed_exist = False
    feed_name = f"\n[markata.feeds.{feed_name}]"
    with open('markata.toml', 'a+') as f:
        for i in f.readlines():
            if i == feed_name:
                feed_exist = True
        if not feed_exist:
            f.write(feed_name)
            f.write(f"""
template='plugins/archive_template.html'
filter="{feed_filter}"
""")

def inputCustomFeed(request):
    form = CustomFeedsForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            feed_info = form.cleaned_data
            feed_name = feed_info.get('name')
            feed_filter = feed_info.get('filter')
            customFeedGenerator(feed_name, feed_filter)
            build(request)
            removeCusotmFeed(feed_name)
        return render(request, 'markout/archive/index.html')
    context = {'form': form}
    return render(request, 'templates/blog/create_feed.html', context)

def removeCusotmFeed(feed_name):
    with open('markata.toml', 'r') as f:
        lines = f.readlines()

    with open('markata.toml', 'w') as f:
        for i in range(len(lines)):
            if lines[i].strip("\n") != f"[markata.feeds.{feed_name}]":
                f.write(lines[i])
            else:
                i+=3

