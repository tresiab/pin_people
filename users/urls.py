from django.urls import path

from .views import location_view, profile_change_view, profile_view

urlpatterns = [
    path("location/", location_view, name="location"),
    path("profile/", profile_view, name="profile"),
    path("profile/change/", profile_change_view, name="profile_change"),
    path("<int:user_id>/", profile_view, name="user_detail"),
    path("<int:user_id>/change/", profile_change_view, name="user_change"),
]
