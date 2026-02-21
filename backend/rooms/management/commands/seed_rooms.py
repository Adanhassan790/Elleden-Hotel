from django.core.management.base import BaseCommand
from rooms.models import RoomType, Room


class Command(BaseCommand):
    help = 'Seeds the database with initial room types and rooms'

    def handle(self, *args, **options):
        self.stdout.write('Seeding room data...')
        
        # Room Types based on website
        room_types_data = [
            {
                'name': 'Single Room',
                'description': 'Comfortable single room perfect for solo travelers. Features a cozy single bed, '
                              'modern amenities, and all the essentials for a relaxing stay.',
                'base_price': 3500.00,
                'max_occupancy': 1,
                'has_wifi': True,
                'has_tv': True,
                'has_ac': False,
                'has_minibar': False,
                'has_workspace': True,
                'has_ensuite': True,
            },
            {
                'name': 'Double Room',
                'description': 'Spacious double room with a queen-size bed, ideal for couples. '
                              'Enjoy premium comfort with modern amenities and a warm atmosphere.',
                'base_price': 5000.00,
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
                'description': 'Perfect for friends or colleagues traveling together. Features two comfortable '
                              'single beds and all modern amenities for a pleasant stay.',
                'base_price': 5500.00,
                'max_occupancy': 2,
                'has_wifi': True,
                'has_tv': True,
                'has_ac': True,
                'has_minibar': False,
                'has_workspace': True,
                'has_ensuite': True,
            },
            {
                'name': 'Family Suite',
                'description': 'Generous family suite with multiple beds, perfect for families. '
                              'Spacious living area and all the comforts of home away from home.',
                'base_price': 7500.00,
                'max_occupancy': 4,
                'has_wifi': True,
                'has_tv': True,
                'has_ac': True,
                'has_minibar': True,
                'has_workspace': True,
                'has_ensuite': True,
            },
        ]
        
        room_types = {}
        for rt_data in room_types_data:
            rt, created = RoomType.objects.get_or_create(
                name=rt_data['name'],
                defaults=rt_data
            )
            room_types[rt_data['name']] = rt
            if created:
                self.stdout.write(f'  Created room type: {rt.name}')
            else:
                self.stdout.write(f'  Room type exists: {rt.name}')
        
        # Create sample rooms (50 rooms as per hotel profile)
        rooms_config = [
            # Single Rooms (10)
            *[{'number': f'1{i:02d}', 'type': 'Single Room', 'floor': 1} for i in range(1, 11)],
            # Double Rooms (15)
            *[{'number': f'2{i:02d}', 'type': 'Double Room', 'floor': 2} for i in range(1, 16)],
            # Twin Rooms (15)
            *[{'number': f'3{i:02d}', 'type': 'Twin Room', 'floor': 3} for i in range(1, 16)],
            # Family Suites (10)
            *[{'number': f'4{i:02d}', 'type': 'Family Suite', 'floor': 4} for i in range(1, 11)],
        ]
        
        for room_config in rooms_config:
            room, created = Room.objects.get_or_create(
                room_number=room_config['number'],
                defaults={
                    'room_type': room_types[room_config['type']],
                    'floor': room_config['floor'],
                    'status': 'available',
                }
            )
            if created:
                self.stdout.write(f'  Created room: {room.room_number}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(rooms_config)} rooms!'))
