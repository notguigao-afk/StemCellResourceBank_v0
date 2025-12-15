from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Sample, SiteSettings


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
                'placeholder': _('e.g., IPSC-2024-001')
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': _('Sample name')
            }),
            'sample_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': _('Detailed description of the sample')
            }),
            'source': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Source institution or lab')
            }),
            'donor_info': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': _('Donor information and consent details')
            }),
            'storage_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g., Freezer A, Rack 3, Box 12')
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
                'placeholder': _('Percentage (0-100)')
            }),
            'quality_control_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Quality control test results and notes')
            }),
            'research_use_only': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
    
    def clean_viability(self):
        viability = self.cleaned_data.get('viability')
        if viability is not None:
            if viability < 0 or viability > 100:
                raise forms.ValidationError(_("Viability must be between 0 and 100%"))
        return viability
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError(_("Quantity cannot be negative"))
        return quantity
    
    def clean(self):
        cleaned_data = super().clean()
        expiration_date = cleaned_data.get('expiration_date')
        collection_date = cleaned_data.get('collection_date')
        storage_date = cleaned_data.get('storage_date')
        
        if expiration_date and collection_date:
            if expiration_date < collection_date:
                raise forms.ValidationError(
                    _("Expiration date cannot be before collection date")
                )
        
        if storage_date and collection_date:
            if storage_date < collection_date:
                raise forms.ValidationError(
                    _("Storage date cannot be before collection date")
                )
        
        return cleaned_data


class SiteSettingsForm(forms.ModelForm):
    """Form for editing site settings"""
    
    class Meta:
        model = SiteSettings
        fields = ['logo', 'site_name_en', 'site_name_zh_hant', 'site_name_zh_hans']
        widgets = {
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'site_name_en': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Site name in English'
            }),
            'site_name_zh_hant': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '繁體中文名稱'
            }),
            'site_name_zh_hans': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '简体中文名称'
            }),
        }


class ExportForm(forms.Form):
    """Form for selecting columns to export"""
    
    COLUMN_CHOICES = [
        ('sample_id', _('Sample ID')),
        ('name', _('Sample Name')),
        ('sample_type', _('Sample Type')),
        ('status', _('Status')),
        ('quantity', _('Quantity')),
        ('passage_number', _('Passage Number')),
        ('storage_location', _('Storage Location')),
        ('source', _('Source')),
        ('donor_info', _('Donor Information')),
        ('description', _('Description')),
        ('viability', _('Viability (%)')),
        ('collection_date', _('Collection Date')),
        ('storage_date', _('Storage Date')),
        ('expiration_date', _('Expiration Date')),
        ('quality_control_notes', _('QC Notes')),
        ('research_use_only', _('Research Use Only')),
        ('created_by', _('Created By')),
        ('created_at', _('Created At')),
        ('updated_at', _('Updated At')),
    ]
    
    columns = forms.MultipleChoiceField(
        choices=COLUMN_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        initial=['sample_id', 'name', 'sample_type', 'status', 'quantity', 'storage_location'],
        required=False
    )
