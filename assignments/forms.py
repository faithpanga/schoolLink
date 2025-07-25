# assignments/forms.py

from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["title", "notes", "attachment"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Updated classes for each field type
        self.fields["title"].widget.attrs.update(
            {
                "class": "input input-bordered w-full",  # <-- UPDATED
                "placeholder": "Enter assignment title",
            }
        )
        self.fields["notes"].widget.attrs.update(
            {
                "class": "textarea textarea-bordered w-full",  # <-- UPDATED
                "rows": 4,
                "placeholder": "Write notes for the parent...",
            }
        )
        self.fields["attachment"].widget.attrs.update(
            {
                # This is much cleaner and theme-aware than the old utility classes
                "class": "file-input file-input-bordered w-full"  # <-- UPDATED
            }
        )
