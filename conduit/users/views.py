from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import redirect


class Login(LoginView):
    template_name = "login.html"
    next_page = reverse_lazy("home")
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.next_page)
        return super().get(request, *args, **kwargs)
    

class Logout(LogoutView):
    next_page = reverse_lazy("home")


class SignUpView(CreateView):
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
    
