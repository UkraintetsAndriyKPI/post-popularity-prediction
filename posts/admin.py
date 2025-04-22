from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'platform', 'title', 'timestamp', 'likes', 'comments')
    search_fields = ('title', 'platform', 'user_id__username')
    list_filter = ('platform', 'timestamp')
    ordering = ('-timestamp',)

    # Optional: Show embedded prediction as readable text
    def predicted_mood(self, obj):
        return obj.prediction.predicted_mood if obj.prediction else 'N/A'

    def predicted_likes(self, obj):
        return obj.prediction.predicted_likes if obj.prediction else 0
