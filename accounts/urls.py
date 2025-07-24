from django.urls import path, include
from . import views

urlpatterns = [
    path("register/", views.teacher_register, name="teacher_register"),
    path("login/", views.custom_login, name="login"),
    path("logout/", views.custom_logout, name="logout"),
    path(
        "setup/<uidb64>/<token>/",
        views.setup_new_parent_account,
        name="setup_parent_account",
    ),
    # Include Django's built-in auth URLs for password reset
    path("password_reset/", include("django.contrib.auth.urls")),
]
