from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["title", "notes", "attachment"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update(
            {
                "class": "w-full p-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-purple-500",
                "placeholder": "Enter assignment title",
            }
        )
        self.fields["notes"].widget.attrs.update(
            {
                "class": "w-full p-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-purple-500",
                "rows": 4,
                "placeholder": "Write notes for the parent...",
            }
        )
        self.fields["attachment"].widget.attrs.update(
            {
                "class": "w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100"
            }
        )
