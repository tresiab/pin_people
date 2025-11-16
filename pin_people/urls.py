"""
URL configuration for pin_people project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic import RedirectView

from users.admin import admin_site
from users.views import register_view

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("images/favicon.ico"))),
    # permanent=False return HTTP 302 instead of HTTP 301
    # 302 - because users may later go to / again after logging out
    path("", RedirectView.as_view(url="/login/", permanent=False)),
    path("admin/", admin_site.urls),
    path("users/", include("users.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/login/"), name="logout"),
    path("register/", register_view, name="register"),
]
