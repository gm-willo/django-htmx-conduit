from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from conduit.articles.forms import ArticleForm, CommentForm

from .models import Article, Comment


def home(request):
    """View all published articles for the global feed"""

    global_feed = Article.objects.order_by("-created_at")
    context = {"global_feed": global_feed}

    if request.user.is_authenticated:
        context["follows_feed"] = Article.objects.filter(
            author__in=request.user.profile.follows.all()
        ).order_by("-created_at")
    else:
        context["follows_feed"] = None

    return render(request, "home.html", context)


def article_detail(request, slug, uuid):
    """Detail view for individual articles"""

    form = CommentForm()

    article = get_object_or_404(Article, slug=slug, uuid=uuid)
    context = {"article": article, "form": form}

    if request.user.is_authenticated:
        context["is_following"] = request.user.profile.is_following(article.author)

    return render(request, "article_detail.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def article_create(request):
    """View for creating articles"""

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
    """View for editing articles"""

    article = get_object_or_404(Article, slug=slug, uuid=uuid)

    if article.author != request.user.profile:
        return HttpResponseForbidden(
            "You've not the permission to modify this article."
        )

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
    """View for deleting articles"""

    article = get_object_or_404(Article, slug=slug, uuid=uuid)

    if article.author != request.user.profile:
        return HttpResponseForbidden(
            "You've not the permission to delete this article."
        )

    if request.method == "POST":
        article.delete()
        return redirect("home")

    return render(request, "article_detail.html", {"article": article})


@login_required
@require_http_methods(["POST"])
def comment_create(request, slug, uuid):
    """View for creating comments"""

    article = get_object_or_404(Article, slug=slug, uuid=uuid)

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user.profile
        comment.article = article
        comment.save()
        return redirect(comment.get_absolute_url())

    return render(request, "article_detail.html", {"article": article})


@login_required
@require_http_methods(["GET", "POST"])
def comment_delete(request, slug, uuid, pk):
    """View for deleting comments"""

    article = get_object_or_404(Article, slug=slug, uuid=uuid)
    comment = get_object_or_404(Comment, pk=pk)

    if comment.author != request.user.profile:
        return HttpResponseForbidden(
            "You've not the permission to delete this comment."
        )

    if request.method == "POST":
        comment.delete()
        return redirect(comment.get_absolute_url())

    return render(request, "article_detail.html", {"article": article})


@login_required
@require_http_methods(["POST"])
def article_favorite(request, slug, uuid):
    """View for adding or deleting an article from favorites"""
    
    article = get_object_or_404(Article, slug=slug, uuid=uuid)
    
    if request.user.profile.has_favorited(article):
        request.user.profile.unfavorite(article)
    else:
        request.user.profile.favorite(article)

    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    
    return redirect("article_detail", slug=slug, uuid=uuid)
