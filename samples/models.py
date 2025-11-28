from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Sample(models.Model):
    """Model representing a stem cell sample in the resource bank"""
    
    SAMPLE_TYPE_CHOICES = [
        ('IPSC', 'Induced Pluripotent Stem Cell'),
        ('ESC', 'Embryonic Stem Cell'),
        ('MSC', 'Mesenchymal Stem Cell'),
        ('HSC', 'Hematopoietic Stem Cell'),
        ('NSC', 'Neural Stem Cell'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('IN_USE', 'In Use'),
        ('DEPLETED', 'Depleted'),
        ('RESERVED', 'Reserved'),
        ('QUARANTINE', 'Quarantine'),
    ]
    
    # Basic Information
    sample_id = models.CharField(max_length=50, unique=True, verbose_name="Sample ID")
    name = models.CharField(max_length=200, verbose_name="Sample Name")
    sample_type = models.CharField(
        max_length=10, 
        choices=SAMPLE_TYPE_CHOICES, 
        default='IPSC',
        verbose_name="Sample Type"
    )
    
    # Description and Details
    description = models.TextField(blank=True, verbose_name="Description")
    source = models.CharField(max_length=200, blank=True, verbose_name="Source")
    donor_info = models.TextField(blank=True, verbose_name="Donor Information")
    
    # Storage and Status
    storage_location = models.CharField(max_length=200, verbose_name="Storage Location")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='AVAILABLE',
        verbose_name="Status"
    )
    quantity = models.FloatField(default=0.0, verbose_name="Quantity (vials)")
    passage_number = models.IntegerField(null=True, blank=True, verbose_name="Passage Number")
    
    # Dates
    collection_date = models.DateField(null=True, blank=True, verbose_name="Collection Date")
    storage_date = models.DateField(default=timezone.now, verbose_name="Storage Date")
    expiration_date = models.DateField(null=True, blank=True, verbose_name="Expiration Date")
    
    # Quality and Characterization
    viability = models.FloatField(null=True, blank=True, verbose_name="Viability (%)")
    quality_control_notes = models.TextField(blank=True, verbose_name="Quality Control Notes")
    
    # Additional Information
    research_use_only = models.BooleanField(default=True, verbose_name="Research Use Only")
    image = models.ImageField(upload_to='sample_images/', blank=True, null=True, verbose_name="Sample Image")
    
    # Metadata
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_samples',
        verbose_name="Created By"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sample"
        verbose_name_plural = "Samples"
    
    def __str__(self):
        return f"{self.sample_id} - {self.name}"
    
    def is_available(self):
        """Check if sample is available for use"""
        return self.status == 'AVAILABLE' and self.quantity > 0
    
    def get_status_badge_class(self):
        """Return CSS class for status badge"""
        status_classes = {
            'AVAILABLE': 'success',
            'IN_USE': 'warning',
            'DEPLETED': 'danger',
            'RESERVED': 'info',
            'QUARANTINE': 'secondary',
        }
        return status_classes.get(self.status, 'secondary')
