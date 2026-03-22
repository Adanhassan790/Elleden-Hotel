"""
Management command to seed the database with sample room types.
Run with: python manage.py seed_room_types
"""
from django.core.management.base import BaseCommand
from rooms.models import RoomType, Room


class Command(BaseCommand):
    help = 'Create sample room types and rooms'

    def handle(self, *args, **options):
        # Create room types if they don't exist
        room_types_data = [
            {
                'name': 'Single Room',
                'description': 'Cozy room perfect for solo travelers. Features a single bed, modern amenities, and comfortable workspace.',
                'base_price': 4500,
                'max_occupancy': 1,
                'has_wifi': True,
                'has_tv': True,
                'has_ac': True,
                'has_minibar': False,
                'has_workspace': True,
                'has_ensuite': True,
            },
            {
                'name': 'Double Room',
                'description': 'Spacious room with a queen-size bed, ideal for couples. Includes all modern amenities and bathroom with shower.',
                'base_price': 6500,
                'max_occupancy': 2,
                'has_wifi': True,
                'has_tv': True,
                'has_ac': True,
                'has_minibar': True,
                'has_workspace': True,
                'has_ensuite': True,
            },
            {
                'name': 'Twin Room',
                'description': 'Two single beds in a comfortable room. Perfect for friends or colleagues traveling together.',
                'base_price': 6500,
                'max_occupancy': 2,
                'has_wifi': True,
                'has_tv': True,
                'has_ac': True,
                'has_minibar': False,
                'has_workspace': True,
                'has_ensuite': True,
            },
            {
                'name': 'Family Room',
                'description': 'Large room with multiple beds, perfect for families. Includes living area, kitchenette, and premium amenities.',
                'base_price': 9500,
                'max_occupancy': 4,
                'has_wifi': True,
                'has_tv': True,
                'has_ac': True,
                'has_minibar': True,
                'has_workspace': True,
                'has_ensuite': True,
            },
        ]

        created_count = 0
        for data in room_types_data:
            room_type, created = RoomType.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'base_price': data['base_price'],
                    'max_occupancy': data['max_occupancy'],
                    'has_wifi': data['has_wifi'],
                    'has_tv': data['has_tv'],
                    'has_ac': data['has_ac'],
                    'has_minibar': data['has_minibar'],
                    'has_workspace': data['has_workspace'],
                    'has_ensuite': data['has_ensuite'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {room_type.name}'))
            else:
                self.stdout.write(f'→ Already exists: {room_type.name}')

        # Create sample rooms for each room type
        room_created_count = 0
        room_numbers = {
            'Single Room': ['101', '102', '103', '104', '105'],
            'Double Room': ['201', '202', '203', '204', '205', '206', '207', '208'],
            'Twin Room': ['301', '302', '303', '304', '305', '306'],
            'Family Room': ['401', '402', '403', '404'],
        }

        for room_type_name, numbers in room_numbers.items():
            room_type = RoomType.objects.get(name=room_type_name)
            for number in numbers:
                room, created = Room.objects.get_or_create(
                    room_number=number,
                    defaults={
                        'room_type': room_type,
                        'floor': int(number[0]),
                        'status': 'available',
                        'is_active': True,
                    }
                )
                if created:
                    room_created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Created: Room {number} ({room_type_name})'))
                else:
                    self.stdout.write(f'→ Already exists: Room {number}')

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Seeding complete!\n'
            f'   Created {created_count} room types\n'
            f'   Created {room_created_count} rooms'
        ))
