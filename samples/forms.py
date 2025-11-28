from django import forms
from .models import Sample


class SampleForm(forms.ModelForm):
    """Form for creating and editing samples"""
    
    class Meta:
        model = Sample
        fields = [
            'sample_id', 'name', 'sample_type', 'description', 'source', 
            'donor_info', 'storage_location', 'status', 'quantity', 
            'passage_number', 'collection_date', 'storage_date', 
            'expiration_date', 'viability', 'quality_control_notes', 
            'research_use_only', 'image'
        ]
        widgets = {
            'sample_id': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., IPSC-2024-001'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Sample name'
            }),
            'sample_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Detailed description of the sample'
            }),
            'source': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Source institution or lab'
            }),
            'donor_info': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Donor information and consent details'
            }),
            'storage_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Freezer A, Rack 3, Box 12'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0'
            }),
            'passage_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'collection_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'storage_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'expiration_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'viability': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '100',
                'placeholder': 'Percentage (0-100)'
            }),
            'quality_control_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Quality control test results and notes'
            }),
            'research_use_only': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

