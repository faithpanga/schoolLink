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
    """
    The definitive, corrected registration form for Teachers.
    This version correctly uses the Meta class to define model fields
    and lets the parent UserCreationForm handle the password fields.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        # Tell the form to use these fields from your User model.
        # The UserCreationForm will AUTOMATICALLY add the password fields itself.
        fields = ("first_name", "last_name", "email", "phone_number")

    def __init__(self, *args, **kwargs):
        # This is where all the fields are created.
        super().__init__(*args, **kwargs)

        # Now that super() has run, all fields exist, including the password fields.
        # We can now safely loop through them to apply styling.
        for field_name, field in self.fields.items():

            # Use a dictionary for cleaner placeholder mapping
            placeholders = {
                "first_name": "Your first name",
                "last_name": "Your last name",
                "email": "your.email@example.com",
                "phone_number": "Your phone number",
                "new_password1": "Create a strong password",
                "new_password2": "Confirm your password",
            }

            field.widget.attrs.update(
                {
                    "class": "input input-bordered w-full",
                    "placeholder": placeholders.get(field_name, ""),  # Set placeholder
                }
            )

            # Add the special ID for the phone number field's JavaScript
            if field_name == "phone_number":
                field.widget.attrs["id"] = "phone_number_input"

    def save(self, commit=True):
        # This method is correct, no changes needed here.
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
