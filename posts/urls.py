from django.urls import path

from .views import post_attempt, prediction_detail

urlpatterns = [
    path("attempt/", post_attempt, name="post_attempt"),
    path('prediction_detail/<str:pk>/', prediction_detail, name='prediction_detail'),
]
