from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["title", "notes", "attachment"]

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"class": "w-full p-2 border border-gray-300 rounded-md shadow-sm"}
        )
        self.fields["notes"].widget.attrs.update(
            {
                "class": "w-full p-2 border border-gray-300 rounded-md shadow-sm",
                "rows": 4,
            }
        )
        self.fields["attachment"].widget.attrs.update(
            {
                "class": "w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            }
        )
