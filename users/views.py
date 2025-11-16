import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

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
    users_qs = User.objects.exclude(latitude=None, longitude=None)
    users = []
    for u in users_qs:
        users.append(
            {
                "id": u.id,
                "username": u.username,
                "latitude": float(u.latitude),
                "longitude": float(u.longitude),
                "position": u.position,
            }
        )
    context = {
        "users_json": json.dumps(list(users)),
        "logged_in_user_id": request.user.id,
        "is_superuser": request.user.is_superuser,
    }
    return render(request, "users/location.html", context)


@login_required(login_url="login")
def profile_view(request, user_id=None):
    """
    Show a user's profile. If user_id is provided, show that user's profile;
    otherwise, show the logged-in user's profile.
    """
    if user_id:
        user = get_object_or_404(User, pk=user_id)
    else:
        user = request.user
    return render(request, "users/profile.html", {"user": user})


@login_required(login_url="login")
def profile_change_view(request, user_id=None):
    """
    Update a user's profile.  If user_id is provided, update that user's profile;
    otherwise, update the logged-in user's profile.
    """
    if user_id:
        user = get_object_or_404(User, pk=user_id)
    else:
        user = request.user

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_detail", user_id=user.id)
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, "users/profile_change.html", {"form": form, "user": user})
