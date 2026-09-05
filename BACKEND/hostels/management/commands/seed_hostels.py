from django.core.management.base import BaseCommand
from hostels.models import Hostel

class Command(BaseCommand):
    help = 'Seed hostels: Lurambi, Sichirai, Kefinco with multiple images'

    def handle(self, *args, **kwargs):
        hostels_data = [
            {
                'name': 'Lurambi Hostel',
                'description': 'Affordable and secure hostel located in Lurambi area, just 1 km from MMUST main gate.',
                'location': 'Lurambi, Kakamega',
                'distance': '1.0 km',
                'price_per_semester': '12000.00',
                'rooms_available': 15,
                'total_rooms': 20,
                'gender': 'Mixed',
                'amenities': ['Wi-Fi', 'Water', 'Electricity', 'Security'],
                'images': [
                    '/static/assets/images/lurambi.jpg',
                    '/static/assets/images/lurambi.jpg',
                    '/static/assets/images/lurambi.jpg',
                ],
                'rating': 4.2,
                'contact': '+254700111333',
            },
            {
                'name': 'Sichirai Hostel',
                'description': 'Modern hostel in the quiet Sichirai neighbourhood.',
                'location': 'Sichirai, Kakamega',
                'distance': '1.5 km',
                'price_per_semester': '18000.00',
                'rooms_available': 8,
                'total_rooms': 12,
                'gender': 'Female',
                'amenities': ['Wi-Fi', 'Water', 'Electricity', 'Security', 'Cafeteria'],
                'images': [
                    '/static/assets/images/sichirai.jpg',
                    '/static/assets/images/sichirai.jpg',
                    '/static/assets/images/sichirai.jpg',
                ],
                'rating': 4.5,
                'contact': '+254722444555',
            },
            {
                'name': 'Kefinco Hostel',
                'description': 'Budget-friendly hostel located near Kefinco.',
                'location': 'Kefinco, Kakamega',
                'distance': '0.8 km',
                'price_per_semester': '10000.00',
                'rooms_available': 20,
                'total_rooms': 25,
                'gender': 'Male',
                'amenities': ['Water', 'Electricity', 'Security'],
                'images': [
                    '/static/assets/images/kefinco.jpg',
                    '/static/assets/images/kefinco.jpg',
                    '/static/assets/images/kefinco.jpg',
                ],
                'rating': 3.9,
                'contact': '+254733666777',
            },
        ]

        for data in hostels_data:
            hostel, created = Hostel.objects.get_or_create(name=data['name'], defaults=data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created hostel: {hostel.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Hostel already exists: {hostel.name}'))