from django.shortcuts import get_object_or_404, render

from .models import Article


def home(request):
    """View all published articles for the global feed."""

    articles = Article.objects.order_by("-created_at")
    context = {"articles": articles}
    return render(request, "home.html", context)


def article_detail(request, slug, uuid):
    """Detail view for individual articles."""

    article = get_object_or_404(Article, slug=slug, uuid=uuid)
    context = {"article": article}
    return render(request, "article_detail.html", context)
