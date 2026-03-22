"""
Management command to seed catering packages.
Run with: python manage.py seed_catering_packages
"""
from django.core.management.base import BaseCommand
from pages.models import CateringPackage


class Command(BaseCommand):
    help = 'Create sample catering packages'

    def handle(self, *args, **options):
        packages_data = [
            {
                'name': 'Budget Package',
                'description': 'Affordable catering option perfect for small gatherings and events on a budget.',
                'price_per_person': 800,
                'minimum_guests': 20,
                'menu_items': 'Main course (chicken or beef), Two sides, Vegetable salad, Soft drinks',
                'is_active': True,
            },
            {
                'name': 'Standard Package',
                'description': 'Our most popular option with a variety of dishes and professional service.',
                'price_per_person': 1200,
                'minimum_guests': 20,
                'menu_items': 'Choice of Main (chicken, beef, or fish), Three sides, Garden salad, Dessert, Soft drinks, Water',
                'is_active': True,
            },
            {
                'name': 'Premium Package',
                'description': 'Elegant catering with premium ingredients and sophisticated presentation.',
                'price_per_person': 1800,
                'minimum_guests': 30,
                'menu_items': 'Premium main course (choice of beef, lamb, or seafood), Four sides, Soup course, Salad, Dessert, Coffee/Tea service, Beverages',
                'is_active': True,
            },
            {
                'name': 'Deluxe Package',
                'description': 'Ultimate luxury catering with exclusive menu and white-glove service.',
                'price_per_person': 2500,
                'minimum_guests': 40,
                'menu_items': 'Appetizers, Premium choice of main courses (beef, lamb, seafood, or vegetarian), Five luxury sides, Soup, Salad, Dessert bar, Coffee/Tea service, Full beverage service, Table service staff included',
                'is_active': True,
            },
            {
                'name': 'Breakfast Package',
                'description': 'Perfect for morning events and conferences. Includes breakfast items and beverages.',
                'price_per_person': 600,
                'minimum_guests': 20,
                'menu_items': 'Assorted pastries, Fresh fruit, Cereals, Coffee, Tea, Juice, Milk',
                'is_active': True,
            },
            {
                'name': 'BBQ Package',
                'description': 'Outdoor BBQ catering with grilled meats and rustic sides.',
                'price_per_person': 1400,
                'minimum_guests': 30,
                'menu_items': 'Grilled chicken, Grilled beef, Grilled sausages, BBQ sauce, Corn on the cob, Potato salad, Coleslaw, Grilled vegetables, Soft drinks, Water',
                'is_active': True,
            },
        ]

        created_count = 0
        for data in packages_data:
            package, created = CateringPackage.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'price_per_person': data['price_per_person'],
                    'minimum_guests': data['minimum_guests'],
                    'menu_items': data['menu_items'],
                    'is_active': data['is_active'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {package.name} (KES {package.price_per_person}/person)')
                )
            else:
                self.stdout.write(f'→ Already exists: {package.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Seeding complete! Created {created_count} catering packages'
        ))
