from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            _ = form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required(login_url="login")
def location_view(request):
    users = User.objects.exclude(latitude=None, longitude=None).values(
        "username", "latitude", "longitude"
    )
    return render(request, "users/location.html", {"users": list(users)})


@login_required(login_url="login")
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})


@login_required(login_url="login")
def profile_change_view(request):
    """
    Allow the logged in user to edit their profile.
    """
    user = request.user
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, "users/profile_change.html", {"form": form})
