from django.urls import path, include
from .views import welcome

app_name = "dashboard"

urlpatterns = [
    path('', welcome, name="welcome"),
]