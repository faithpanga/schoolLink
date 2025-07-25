# students/forms.py

from django import forms
from phonenumber_field.formfields import PhoneNumberField  # <-- CORRECTED IMPORT


class AddStudentForm(forms.Form):
    student_first_name = forms.CharField(max_length=100, label="Student's First Name")
    student_last_name = forms.CharField(max_length=100, label="Student's Last Name")
    parent_first_name = forms.CharField(max_length=100, label="Parent's First Name")
    parent_last_name = forms.CharField(max_length=100, label="Parent's Last Name")
    parent_email = forms.EmailField(label="Parent's Email Address")

    # The parent_phone field now lives here, where it belongs.
    parent_phone = PhoneNumberField(
        label="Parent's Phone Number",
        widget=forms.TextInput(attrs={"id": "parent_phone_input"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This loop applies the correct DaisyUI class to all fields.
        for name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "input input-bordered w-full",
                }
            )
