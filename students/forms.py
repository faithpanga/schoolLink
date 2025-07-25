# students/forms.py

from django import forms
from phonenumber_field.formfields import PhoneNumberField


# students/forms.py
import re
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python


class AddStudentForm(forms.Form):
    """
    The definitive form for adding a student.
    It now automatically formats the phone number on the backend.
    """

    student_first_name = forms.CharField(label="Student's First Name")
    student_last_name = forms.CharField(label="Student's Last Name")
    parent_first_name = forms.CharField(label="Parent's First Name")
    parent_last_name = forms.CharField(label="Parent's Last Name")
    parent_email = forms.EmailField(label="Parent's Email Address")

    # We use a standard CharField for input to capture the raw number
    parent_phone = forms.CharField(
        label="Parent's Phone Number",
        required=False,
        help_text="Enter a local number (e.g., 712345678) or an international one (e.g., +14155552671).",
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g., 712 345 678",
                "type": "tel",  # Use the 'tel' input type for better mobile usability
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply DaisyUI classes to all fields
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input input-bordered w-full"})

    def clean_parent_phone(self):
        """
        This method cleans and validates the phone number.
        - Strips formatting characters.
        - Adds '+255' if a country code is not provided.
        - Validates the final number.
        """
        phone = self.cleaned_data.get("parent_phone")

        if phone:
            # First, strip out common formatting characters like spaces, dashes, and parentheses
            phone = re.sub(r"[\s\(\)-]", "", phone)

            # If the cleaned number doesn't start with '+', assume it's a local TZ number
            if not phone.startswith("+"):
                # Prepend the +255 country code
                phone = f'+255{phone.lstrip("0")}'  # Also strips a leading 0 if present

            # Now, validate the complete number using the phonenumbers library
            try:
                phone_number_obj = to_python(phone)
                if phone_number_obj.is_valid():
                    return phone_number_obj  # Return the valid PhoneNumber object
                else:
                    raise forms.ValidationError("Please enter a valid phone number.")
            except Exception:
                raise forms.ValidationError("The phone number format is invalid.")

        return phone  # Return the empty value if nothing was entered
