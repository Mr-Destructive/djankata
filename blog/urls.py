from django.urls import path
from .views import archives

urlpatterns = [
        path('', archives),
]
