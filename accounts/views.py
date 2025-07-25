from django.utils import timezone  # This is Django's time-aware utility
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import LoginForm, TeacherRegistrationForm
from .models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def home_view(request):
    if request.user.is_authenticated:
        if request.user.role == "TEACHER":
            return redirect("teacher_dashboard")
        elif request.user.role == "PARENT":
            return redirect("parent_dashboard")
    return render(request, "home.html")


def teacher_register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect("home")
    else:
        form = TeacherRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def custom_login(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)  # Bind data to the form
        if form.is_valid():
            identifier = form.cleaned_data.get("identifier")
            password = form.cleaned_data.get("password")
            user = None

            try:  # Use email to authenticate
                user = authenticate(request, email=identifier, password=password)
            except:
                pass

            if not user:  # If email fails, try phone
                try:
                    user_by_phone = User.objects.get(phone_number=identifier)
                    if user_by_phone.check_password(password):
                        user = authenticate(
                            request, email=user_by_phone.email, password=password
                        )
                except User.DoesNotExist:
                    pass

            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome back, {user.first_name}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = LoginForm()  # Create an unbound form for GET requests

    # Pass the form to the template
    return render(request, "accounts/login.html", {"form": form})


def custom_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


def send_account_setup_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    setup_link = request.build_absolute_uri(f"/accounts/setup/{uid}/{token}/")

    context = {
        "user": user,
        "setup_link": setup_link,
        "current_year": timezone.now().year,
    }

    subject = "Welcome to SchoolLink! Set Up Your Account"
    message = render_to_string("accounts/email/account_setup_email.html", context)

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def setup_new_parent_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password = request.POST.get("password")
            password_confirm = request.POST.get("password_confirm")
            if password and password == password_confirm:
                user.set_password(password)
                user.save()
                messages.success(
                    request, "Your password has been set! You can now log in."
                )
                return redirect("login")
            else:
                messages.error(request, "Passwords do not match. Please try again.")
        return render(request, "accounts/setup_parent_account.html")
    else:
        messages.error(request, "The account setup link is invalid or has expired.")
        return redirect("home")
