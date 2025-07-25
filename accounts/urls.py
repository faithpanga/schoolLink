from django.urls import path, include
from accounts.forms import CustomPasswordResetForm, CustomSetPasswordForm  # <-- IMPORT
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.teacher_register, name="teacher_register"),
    path("login/", views.custom_login, name="login"),
    path("logout/", views.custom_logout, name="logout"),
    path(
        "setup/<uidb64>/<token>/",
        views.setup_new_parent_account,
        name="setup_parent_account",
    ),  # --- PASSWORD RESET URLS ---
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            form_class=CustomPasswordResetForm,  # <-- USE YOUR CUSTOM FORM
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            form_class=CustomSetPasswordForm,  # <-- USE YOUR CUSTOM FORM
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
