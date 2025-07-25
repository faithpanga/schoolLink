from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "date"]
        # Use Django's built-in datetime widget
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply DaisyUI classes for a beautiful, consistent look
        self.fields["title"].widget.attrs.update(
            {
                "class": "input input-bordered w-full",
                "placeholder": "e.g., Parent-Teacher Conference",
            }
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "textarea textarea-bordered w-full",
                "rows": 5,
                "placeholder": "Enter the event details here...",
            }
        )
        self.fields["date"].widget.attrs.update(
            {"class": "input input-bordered w-full"}
        )
