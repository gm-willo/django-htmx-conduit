from django.db import models
from django.shortcuts import reverse

from django.utils.text import slugify
import uuid


class Article(models.Model):
    """Article model."""

    # when we do queries on articles in out db, we'll often be loooking at the title,
    # so having this field as index will speed the queries
    title = models.CharField(db_index=True, max_length=255)
    slug = models.SlugField(max_length=100, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField(max_length=2000)
    body = models.TextField()
    author = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="articles",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug, "uuid": self.uuid})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)