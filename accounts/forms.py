# accounts/forms.py

from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField  # <-- CORRECT IMPORT
from .models import User


class LoginForm(forms.Form):
    """
    A custom login form to allow login with email or phone number.
    """

    identifier = forms.CharField(
        label="Email or Phone Number",
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",  # DaisyUI class
                "placeholder": "e.g., user@example.com or +255...",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "input input-bordered w-full",  # DaisyUI class
                "placeholder": "••••••••",
            }
        ),
    )


class TeacherRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email", "phone_number")

    # The phone_number field is no longer defined here.
    # We will modify the one created by the Meta class below.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We will style each field explicitly for clarity and control.
        self.fields["first_name"].widget.attrs.update(
            {"class": "input input-bordered w-full"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"class": "input input-bordered w-full"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "input input-bordered w-full"}
        )

        # This is the correct way to modify the phone_number field
        self.fields["phone_number"].widget.attrs.update(
            {
                "class": "input input-bordered w-full",
                "id": "phone_number_input",  # The ID for our JavaScript
            }
        )

        # Style the default password fields from UserCreationForm
        self.fields["password"].widget.attrs.update(
            {"class": "input input-bordered w-full"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "input input-bordered w-full"}
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.TEACHER
        if commit:
            user.save()
        return user


class SetPasswordForm(forms.Form):
    """
    A form for a user to set their password for the first time.
    """

    password = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "input input-bordered w-full",  # DaisyUI class
                "placeholder": "••••••••",
            }
        ),
    )
    password_confirm = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "input input-bordered w-full",  # DaisyUI class
                "placeholder": "••••••••",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("The two password fields didn't match.")
        return cleaned_data


class CustomPasswordResetForm(auth_forms.PasswordResetForm):
    """
    Subclasses the default PasswordResetForm to add DaisyUI styling.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "class": "input input-bordered w-full",  # DaisyUI class
                "placeholder": "Enter your email address",
            }
        )


class CustomSetPasswordForm(auth_forms.SetPasswordForm):
    """
    Subclasses the default SetPasswordForm to add DaisyUI styling.
    This is used in the password reset confirmation link.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "input input-bordered w-full",  # DaisyUI class
                "placeholder": "••••••••",
            }
        )
        self.fields["new_password2"].widget.attrs.update(
            {
                "class": "input input-bordered w-full",  # DaisyUI class
                "placeholder": "••••••••",
            }
        )
