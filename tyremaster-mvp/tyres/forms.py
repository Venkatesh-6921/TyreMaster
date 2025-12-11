from django import forms
from .models import VehicleSubmission

class VehicleSubmissionForm(forms.ModelForm):
    class Meta:
        model = VehicleSubmission
        fields = [
            'user_name', 'user_email', 'user_phone',
            'brand', 'model', 'year', 'category',
            'front_size', 'rear_size', 'tyre_size',
            'front_pressure', 'rear_pressure',
            'source', 'comments'
        ]
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'user_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any additional information...'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1900, 'max': 2025}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        # At least one tyre size should be provided
        front = cleaned_data.get('front_size')
        rear = cleaned_data.get('rear_size')
        tyre = cleaned_data.get('tyre_size')
        
        if not (front or rear or tyre):
            raise forms.ValidationError("Please provide at least one tyre size")
        
        return cleaned_data