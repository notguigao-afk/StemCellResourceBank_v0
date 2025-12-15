from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class SiteSettings(models.Model):
    """Singleton model for site-wide settings like logo"""
    
    logo = models.ImageField(
        upload_to='site/', 
        blank=True, 
        null=True, 
        verbose_name=_("Site Logo")
    )
    site_name_en = models.CharField(
        max_length=200, 
        default="Inventory Management System of Hong Kong Cell and Stem Cell Resource Center",
        verbose_name=_("Site Name (English)")
    )
    site_name_zh_hant = models.CharField(
        max_length=200, 
        default="香港細胞及幹細胞資源中心庫存管理系統",
        verbose_name=_("Site Name (Traditional Chinese)")
    )
    site_name_zh_hans = models.CharField(
        max_length=200, 
        default="香港细胞及干细胞资源中心库存管理系统",
        verbose_name=_("Site Name (Simplified Chinese)")
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        pass  # Prevent deletion
    
    @classmethod
    def get_settings(cls):
        """Get or create the singleton settings instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def __str__(self):
        return "Site Settings"


class Sample(models.Model):
    """Model representing a stem cell sample in the resource bank"""
    
    SAMPLE_TYPE_CHOICES = [
        ('IPSC', _('Induced Pluripotent Stem Cell')),
        ('ESC', _('Embryonic Stem Cell')),
        ('MSC', _('Mesenchymal Stem Cell')),
        ('HSC', _('Hematopoietic Stem Cell')),
        ('NSC', _('Neural Stem Cell')),
        ('OTHER', _('Other')),
    ]
    
    STATUS_CHOICES = [
        ('AVAILABLE', _('Available')),
        ('IN_USE', _('In Use')),
        ('DEPLETED', _('Depleted')),
        ('RESERVED', _('Reserved')),
        ('QUARANTINE', _('Quarantine')),
    ]
    
    # Basic Information
    sample_id = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name=_("Sample ID")
    )
    name = models.CharField(
        max_length=200, 
        verbose_name=_("Sample Name")
    )
    sample_type = models.CharField(
        max_length=10, 
        choices=SAMPLE_TYPE_CHOICES, 
        default='IPSC',
        verbose_name=_("Sample Type")
    )
    
    # Description and Details
    description = models.TextField(
        blank=True, 
        verbose_name=_("Description")
    )
    source = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name=_("Source")
    )
    donor_info = models.TextField(
        blank=True, 
        verbose_name=_("Donor Information")
    )
    
    # Storage and Status
    storage_location = models.CharField(
        max_length=200, 
        verbose_name=_("Storage Location")
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='AVAILABLE',
        verbose_name=_("Status")
    )
    quantity = models.FloatField(
        default=0.0, 
        validators=[MinValueValidator(0)],
        verbose_name=_("Quantity (vials)")
    )
    passage_number = models.IntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name=_("Passage Number")
    )
    
    # Dates
    collection_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name=_("Collection Date")
    )
    storage_date = models.DateField(
        default=timezone.now, 
        verbose_name=_("Storage Date")
    )
    expiration_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name=_("Expiration Date")
    )
    
    # Quality and Characterization
    viability = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Viability (%)")
    )
    quality_control_notes = models.TextField(
        blank=True, 
        verbose_name=_("Quality Control Notes")
    )
    
    # Additional Information
    research_use_only = models.BooleanField(
        default=True, 
        verbose_name=_("Research Use Only")
    )
    image = models.ImageField(
        upload_to='sample_images/', 
        blank=True, 
        null=True, 
        verbose_name=_("Sample Image")
    )
    
    # Metadata
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_samples',
        verbose_name=_("Created By")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_("Updated At")
    )
    
    # History tracking
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Sample")
        verbose_name_plural = _("Samples")
        indexes = [
            models.Index(fields=['sample_id']),
            models.Index(fields=['status']),
            models.Index(fields=['sample_type']),
            models.Index(fields=['-updated_at']),
        ]
    
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
    
    def save(self, *args, **kwargs):
        # Compress image if present
        if self.image:
            self.image = self.compress_image(self.image)
        super().save(*args, **kwargs)
    
    def compress_image(self, image, max_size_kb=500, max_dimension=1200):
        """Compress image to reduce storage usage"""
        if not image:
            return image
        
        try:
            img = Image.open(image)
            
            # Convert to RGB if necessary (for PNG with transparency)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            if img.width > max_dimension or img.height > max_dimension:
                img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            
            # Save with compression
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # Create new file
            return InMemoryUploadedFile(
                output,
                'ImageField',
                f"{image.name.rsplit('.', 1)[0]}.jpg",
                'image/jpeg',
                sys.getsizeof(output),
                None
            )
        except Exception:
            # If compression fails, return original
            return image
