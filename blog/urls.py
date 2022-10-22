from django.urls import path
from .views import archives
from django.conf.urls.static import static
from djankata import settings


urlpatterns = [
        path('', archives),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
