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
    A custom UserCreationForm for Teachers.
    We explicitly define all fields to ensure they exist before styling.
    """

    # Explicitly define the fields we want to add or control
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(label="Email Address")
    phone_number = PhoneNumberField(
        label="Phone Number", widget=forms.TextInput(attrs={"id": "phone_number_input"})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # The fields tuple now includes 'new_password1' and 'new_password2' from the parent form.
        # It should list all fields that the form will handle.
        fields = ("first_name", "last_name", "email", "phone_number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Now that all fields are guaranteed to exist, we can safely style them.
        for field_name, field in self.fields.items():
            # The password fields have different placeholder text
            if field_name == "new_password1":
                placeholder = "Enter password"
            elif field_name == "new_password2":
                placeholder = "Confirm password"
            else:
                placeholder = field.label

            field.widget.attrs.update(
                {
                    "class": "input input-bordered w-full",
                    "placeholder": placeholder,
                }
            )
            # Give the phone number input its special ID for the JS library
            if field_name == "phone_number":
                field.widget.attrs["id"] = "phone_number_input"

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
