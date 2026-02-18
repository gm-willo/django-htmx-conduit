from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import User
from .forms import ProfileForm, UserForm


class Login(LoginView):
    """Class based view for user login"""
    template_name = "login.html"
    next_page = reverse_lazy("home")
    redirect_authenticated_user = True
    

class Logout(LogoutView):
    """Class based view for user logout"""
    next_page = reverse_lazy("home")


class SignUpView(CreateView):
    """Class based view for user signup"""
    model = get_user_model()
    fields = ["username", "email", "password"]
    template_name = "signup.html"
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
        # create the User object
        user = form.save(commit=False)
        # set password manually
        # as otherwise the User will be saved with unhashed password
        password = form.cleaned_data.get("password")
        user.set_password(password)
        # save the User object to the database
        user.save()
        # authenticate your user with unhashed password
        # (`authenticate` expects unhashed passwords)
        email = form.cleaned_data.get("email")
        authenticated_user = authenticate(email=email, password=password)
        login(self.request, authenticated_user)
        return redirect(self.success_url)


def profile_detail(request, username):
    """Detail view for user profiles"""
    
    user = get_object_or_404(User, username=username)
    profile = user.profile
    context = {"profile": profile}
    
    if request.user.is_authenticated:
        context["my_articles"] = profile.articles.order_by("-created_at")
    
    return render(request, "profile_detail.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def profile_update(request):
    """Update view for user profile and account settings"""
    
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        user_form = UserForm(request.POST, instance=request.user)
        
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect("settings")
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = UserForm(instance=request.user)
    
    context = {
        "form": profile_form,
        "user_form": user_form,
    }
    return render(request, "settings.html", context)