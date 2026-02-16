from django.shortcuts import render

from .models import Article


def home(request):
    """View all published articles for the global feed."""
    
    articles = Article.objects.order_by("-created_at")
    context = {"articles": articles}
    return render(request, "home.html", context)
