# events/forms.py

from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "date_time",
            "location",
            "price",
            "category",
        ]
        widgets = {
            "date_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_time"].input_formats = ["%Y-%m-%dT%H:%M"]
        # Add Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
