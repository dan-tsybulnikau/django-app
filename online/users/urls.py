"""online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path, reverse_lazy, reverse

from . import views
from django.contrib.auth import views as auth_views
from . import views
from . import forms

app_name = "users"

urlpatterns = [
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            next_page="store:index", template_name="users/login.html"
        ),
        name="login",
    ),
    path(
        "logout/", auth_views.LogoutView.as_view(next_page="store:index"), name="logout"
    ),
    path(
        "change-pass/",
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy("users:password_change_done"),
            template_name="users/password_change.html",
            form_class=forms.CustomPasswordChangeForm,
        ),
        name="change",
    ),
    path(
        "change-pass-confirm/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_success.html"
        ),
        name="password_change_done",
    ),
    path(
        "password-reset",
        auth_views.PasswordResetView.as_view(
            email_template_name="users/password_reset_mail.html",
            template_name="users/password_reset.html",
            success_url=reverse_lazy("users:pass-reset-done"),
        ),
        name="pass-reset",
    ),
    path(
        "password-reset-done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="pass-reset-done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("users:reset_complete"),
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="reset_complete",
    ),

]
