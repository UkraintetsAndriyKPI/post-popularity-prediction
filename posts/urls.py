from django.urls import path

from .views import post_attempt

urlpatterns = [
    path("attempt/", post_attempt, name="post_attempt"),
]
