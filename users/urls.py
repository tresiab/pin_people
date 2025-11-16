from django.urls import path

from .views import location_view, profile_change_view, profile_view

urlpatterns = [
    path("", location_view, name="location"),
    path("profile/", profile_view, name="profile"),
    path("profile/change/", profile_change_view, name="profile_change"),
]
