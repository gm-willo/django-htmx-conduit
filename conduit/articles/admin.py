from django.contrib import admin
from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ("slug", "uuid")


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)