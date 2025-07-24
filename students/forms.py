from django import forms
from phonenumber_field.formfields import PhoneNumberField


class AddStudentForm(forms.Form):
    student_first_name = forms.CharField(max_length=100, label="Student's First Name")
    student_last_name = forms.CharField(max_length=100, label="Student's Last Name")
    parent_first_name = forms.CharField(max_length=100, label="Parent's First Name")
    parent_last_name = forms.CharField(max_length=100, label="Parent's Last Name")
    parent_email = forms.EmailField(label="Parent's Email Address")
    parent_phone = PhoneNumberField(
        label="Parent's Phone Number",
        help_text="Use E.164 format (e.g., +255712345678)",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "w-full p-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500",
                    "placeholder": field.label,
                }
            )
