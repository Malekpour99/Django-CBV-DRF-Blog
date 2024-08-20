from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView

from .forms import CustomUserCreationForm
from .models import Profile


class RegisterView(FormView):
    """
    Managing registration of new users

    Attributes:
     - email: User's valid email address
     - password1: User's password
     - password2: User's password confirmation
    """

    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("blog:index")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            # login user after successful registration
            login(self.request, user)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    Provides a form for users to update their profile information.
    """

    template_name = "registration/profile.html"
    model = Profile
    fields = ["image", "first_name", "last_name", "username", "bio"]
    success_url = reverse_lazy("accounts:user-profile")

    def get_object(self, queryset=None):
            username = self.kwargs.get('username')
            return get_object_or_404(Profile, username=username)
