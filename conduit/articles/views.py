from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse

from conduit.articles.forms import ArticleForm

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


@login_required
@require_http_methods(["GET", "POST"])
def article_create(request):
    """View for creating articles."""
    
    if request.method == "POST":
        form = ArticleForm(request.POST)
        
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.profile
            article.save()
            return redirect(article.get_absolute_url())
    else:
        form = ArticleForm()
    return render(request, "editor.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def article_update(request, slug, uuid):
    """View for editing articles."""
    
    article = get_object_or_404(Article, slug=slug, uuid=uuid)
    
    if article.author != request.user.profile:
        return HttpResponseForbidden("You've not the permission to modify this article.")
    
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        
        if form.is_valid():
            form.save()
            return redirect(article.get_absolute_url())
    else:
        form = ArticleForm(instance=article)
    return render(request, "editor.html", {"form": form, "article": article})


@login_required
@require_http_methods(["GET", "POST"])
def article_delete(request, slug, uuid):
    """View for deleting articles."""
    
    article = get_object_or_404(Article, slug=slug, uuid=uuid)
    
    if article.author != request.user.profile:
        return HttpResponseForbidden("You've not the permission to delete this article.")
    
    if request.method == "POST":
        article.delete()
        return redirect("home")
    
    return render(request, "article_detail.html", {"article": article})