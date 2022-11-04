import os
from django.urls import path
from .views import ArticleEditMarkdown, archives, build, createArticle, customFeedGenerator, inputCustomFeed
from django.conf.urls.static import static
from djankata import settings

MARKOUT_ROOT = os.path.join(settings.BASE_DIR, 'markout')
MARKOUT_URL = '/'
MARKOUT_DIR = (MARKOUT_URL,)

urlpatterns = [
        path('', archives, name="archive"),
        path('build/', build, name="build"),
        path('add/', createArticle, name='create-article'),
        path('input-feed', inputCustomFeed, name='input-feed-gen'),
        path('generate/', customFeedGenerator, name='custom-feed-gen'),
        path('edit-mark/<str:title>', ArticleEditMarkdown, name='edit-markdown'),
    ] + static(MARKOUT_URL, document_root=MARKOUT_ROOT)
