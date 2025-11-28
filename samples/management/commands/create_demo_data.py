from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from samples.models import Sample
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Create demo data for testing the application'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo data...\n')
        
        # Create Lab Staff group if not exists
        lab_staff_group, _ = Group.objects.get_or_create(name='Lab Staff')
        
        # Create users
        admin_user, admin_created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if admin_created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user (username: admin, password: admin123)'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
        
        lab_staff_user, staff_created = User.objects.get_or_create(
            username='labstaff',
            defaults={
                'email': 'staff@example.com',
                'is_staff': True
            }
        )
        if staff_created:
            lab_staff_user.set_password('staff123')
            lab_staff_user.save()
            lab_staff_user.groups.add(lab_staff_group)
            self.stdout.write(self.style.SUCCESS('Created lab staff user (username: labstaff, password: staff123)'))
        else:
            self.stdout.write(self.style.WARNING('Lab staff user already exists'))
        
        # Create demo samples
        demo_samples = [
            {
                'sample_id': 'IPSC-2024-001',
                'name': 'Human iPSC Line - Patient A',
                'sample_type': 'IPSC',
                'description': 'Induced pluripotent stem cells derived from adult fibroblasts. High quality line with confirmed pluripotency markers.',
                'source': 'Stanford Stem Cell Institute',
                'storage_location': 'Freezer A, Rack 1, Box 5',
                'status': 'AVAILABLE',
                'quantity': 10.0,
                'passage_number': 15,
                'collection_date': date.today() - timedelta(days=180),
                'viability': 95.5,
                'quality_control_notes': 'Karyotype normal. OCT4, SOX2, NANOG positive.',
            },
            {
                'sample_id': 'ESC-2024-002',
                'name': 'Human Embryonic Stem Cell H9',
                'sample_type': 'ESC',
                'description': 'Well-characterized human embryonic stem cell line. Widely used in research.',
                'source': 'WiCell Research Institute',
                'storage_location': 'Freezer B, Rack 2, Box 3',
                'status': 'AVAILABLE',
                'quantity': 8.0,
                'passage_number': 42,
                'collection_date': date.today() - timedelta(days=120),
                'viability': 92.0,
                'quality_control_notes': 'Pluripotency markers confirmed. Mycoplasma negative.',
            },
            {
                'sample_id': 'MSC-2024-003',
                'name': 'Bone Marrow MSC',
                'sample_type': 'MSC',
                'description': 'Mesenchymal stem cells isolated from human bone marrow. Capable of multilineage differentiation.',
                'source': 'Local Hospital Donor Program',
                'storage_location': 'Freezer A, Rack 3, Box 1',
                'status': 'AVAILABLE',
                'quantity': 15.0,
                'passage_number': 5,
                'collection_date': date.today() - timedelta(days=60),
                'viability': 98.2,
                'quality_control_notes': 'CD73, CD90, CD105 positive. CD34, CD45 negative.',
            },
            {
                'sample_id': 'HSC-2024-004',
                'name': 'Cord Blood Hematopoietic Stem Cells',
                'sample_type': 'HSC',
                'description': 'Purified CD34+ hematopoietic stem cells from umbilical cord blood.',
                'source': 'Cord Blood Bank',
                'storage_location': 'Freezer C, Rack 1, Box 2',
                'status': 'RESERVED',
                'quantity': 5.0,
                'collection_date': date.today() - timedelta(days=30),
                'viability': 96.7,
                'quality_control_notes': 'CD34+, CD38- population confirmed by flow cytometry.',
            },
            {
                'sample_id': 'NSC-2024-005',
                'name': 'Neural Stem Cells',
                'sample_type': 'NSC',
                'description': 'Neural stem cells derived from iPSCs. Can differentiate into neurons, astrocytes, and oligodendrocytes.',
                'source': 'In-house Differentiation',
                'storage_location': 'Freezer A, Rack 2, Box 4',
                'status': 'AVAILABLE',
                'quantity': 12.0,
                'passage_number': 8,
                'collection_date': date.today() - timedelta(days=45),
                'viability': 94.3,
                'quality_control_notes': 'Nestin and SOX2 positive. Neural differentiation potential confirmed.',
            },
            {
                'sample_id': 'IPSC-2024-006',
                'name': 'Disease-specific iPSC - Parkinson\'s',
                'sample_type': 'IPSC',
                'description': 'Patient-derived iPSCs from individual with Parkinson\'s disease. Carries LRRK2 mutation.',
                'source': 'Collaborative Research Network',
                'storage_location': 'Freezer B, Rack 1, Box 1',
                'status': 'IN_USE',
                'quantity': 6.0,
                'passage_number': 20,
                'collection_date': date.today() - timedelta(days=90),
                'viability': 93.8,
                'quality_control_notes': 'LRRK2 G2019S mutation confirmed. Pluripotency verified.',
            },
        ]
        
        created_count = 0
        for sample_data in demo_samples:
            sample, created = Sample.objects.get_or_create(
                sample_id=sample_data['sample_id'],
                defaults={
                    **sample_data,
                    'created_by': admin_user,
                    'storage_date': date.today(),
                    'research_use_only': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  Created sample: {sample.sample_id}'))
            else:
                self.stdout.write(self.style.WARNING(f'  Sample already exists: {sample.sample_id}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n=== Demo Data Creation Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} new samples'))
        self.stdout.write(self.style.SUCCESS(f'\nYou can now log in with:'))
        self.stdout.write('  Admin - username: admin, password: admin123')
        self.stdout.write('  Lab Staff - username: labstaff, password: staff123')

