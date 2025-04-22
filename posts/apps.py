from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = 'posts'


    def ready(self):
        from posts.jobs import updater
        updater.start()
