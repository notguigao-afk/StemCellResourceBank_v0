from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from samples.models import Sample


class Command(BaseCommand):
    help = 'Set up user groups with appropriate permissions'

    def handle(self, *args, **options):
        # Get Sample content type
        sample_content_type = ContentType.objects.get_for_model(Sample)
        
        # Create Lab Staff group
        lab_staff_group, created = Group.objects.get_or_create(name='Lab Staff')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Lab Staff group'))
        else:
            self.stdout.write(self.style.WARNING('Lab Staff group already exists'))
        
        # Assign permissions to Lab Staff
        permissions = Permission.objects.filter(content_type=sample_content_type)
        lab_staff_group.permissions.set(permissions)
        
        self.stdout.write(self.style.SUCCESS(
            f'Assigned {permissions.count()} permissions to Lab Staff group'
        ))
        
        self.stdout.write(self.style.SUCCESS('\n=== Setup Complete ==='))
        self.stdout.write(self.style.SUCCESS('Lab Staff group has been configured with permissions to:'))
        self.stdout.write('  - Add samples')
        self.stdout.write('  - Change samples')
        self.stdout.write('  - Delete samples')
        self.stdout.write('  - View samples')

