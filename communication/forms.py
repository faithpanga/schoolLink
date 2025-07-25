# communication/forms.py

from django import forms


class BroadcastForm(forms.Form):
    subject = forms.CharField(
        label="Subject",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "e.g., School Closure Announcement",
            }
        ),
    )
    body = forms.CharField(
        label="Message Body",
        widget=forms.Textarea(
            attrs={
                "class": "textarea textarea-bordered w-full",
                "placeholder": "Write your announcement here...",
                "rows": 6,
            }
        ),
    )
    # Add the checkbox field
    send_sms = forms.BooleanField(
        label="Send SMS Alert to all parents with a phone number",
        required=False,  # Make it optional
        widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
    )


class MessageForm(forms.Form):
    """
    A simple form for sending a reply in a communication log.
    """

    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "textarea textarea-bordered w-full",
                "placeholder": "Type your message here...",
                "rows": 2,
            }
        )
    )
    send_sms = forms.BooleanField(
        label="Send SMS Alert",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
    )
