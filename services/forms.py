# services/forms.py
from django import forms
from .models import Service

INPUT_CLASSES = "w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md shadow-black/30 focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-400"

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["title", "description", "price", "duration_hours", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Service title"}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASSES, "rows": 3, "placeholder": "Describe your service"}),
            "price": forms.NumberInput(attrs={"class": INPUT_CLASSES, "placeholder": "Price (৳)"}),
            "duration_hours": forms.NumberInput(attrs={"class": INPUT_CLASSES, "placeholder": "Duration (hours)"}),
            "image": forms.ClearableFileInput(attrs={"class": "w-full text-sm text-gray-600"}),
        }
