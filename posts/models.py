from django.db import models
from django.contrib.auth.models import User
from django_mongodb_backend.models import EmbeddedModel
from django_mongodb_backend.fields import EmbeddedModelField


class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    platform = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    title = models.TextField()
    content = models.TextField()

    post_creation_timestamp = models.DateTimeField()

    likes = models.IntegerField()
    comments = models.IntegerField()
    views = models.IntegerField(null=True)

    prediction = EmbeddedModelField(embedded_model='Prediction')



class Prediction(EmbeddedModel):
    predicted_likes = models.IntegerField()
    predicted_comments = models.IntegerField()
    predicted_shares = models.IntegerField()
    predicted_mood = models.CharField(max_length=50, default='unpredicted')
