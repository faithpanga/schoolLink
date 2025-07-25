# students/forms.py

from django import forms
from phonenumber_field.formfields import PhoneNumberField


class AddStudentForm(forms.Form):
    """
    The definitive form for adding a student.
    Defaults the phone number to the Tanzanian country code (+255).
    """

    student_first_name = forms.CharField(label="Student's First Name")
    student_last_name = forms.CharField(label="Student's Last Name")
    parent_first_name = forms.CharField(label="Parent's First Name")
    parent_last_name = forms.CharField(label="Parent's Last Name")
    parent_email = forms.EmailField(label="Parent's Email Address")

    # A single, simple field for the phone number.
    parent_phone = PhoneNumberField(
        label="Parent's Phone Number (with country code)",
        required=False,  # Make phone number optional
        initial="+255",  # <-- THIS IS THE FIX: Set the default value
        widget=forms.TextInput(attrs={"id": "parent_phone_input"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply DaisyUI classes to all fields
        for name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "input input-bordered w-full", "placeholder": field.label}
            )
