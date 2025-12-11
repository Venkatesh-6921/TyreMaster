# tyres/management/commands/import_sample_data.py
import os
import django
from django.core.management.base import BaseCommand
from tyres.models import Vehicle, TyreSize

class Command(BaseCommand):
    help = 'Populate database with sample tyre data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Adding sample vehicles...')
        
        # Sample data - Scooters
        scooters = [
            {
                'brand': 'Honda',
                'model': 'Activa 6G',
                'year': 2023,
                'category': 'SCOOTER',
                'front_size': '90/90-12',
                'rear_size': '90/100-10',
                'front_pressure': '29 PSI',
                'rear_pressure': '33 PSI'
            },
            {
                'brand': 'Suzuki',
                'model': 'Access 125',
                'year': 2023,
                'category': 'SCOOTER',
                'front_size': '90/90-12',
                'rear_size': '90/100-10',
                'front_pressure': '29 PSI',
                'rear_pressure': '33 PSI'
            },
            {
                'brand': 'TVS',
                'model': 'Jupiter',
                'year': 2023,
                'category': 'SCOOTER',
                'front_size': '90/90-12',
                'rear_size': '90/100-10',
                'front_pressure': '28 PSI',
                'rear_pressure': '36 PSI'
            },
            {
                'brand': 'Hero',
                'model': 'Pleasure Plus',
                'year': 2023,
                'category': 'SCOOTER',
                'tyre_size': '90/100-10',
                'front_pressure': '25 PSI',
                'rear_pressure': '36 PSI'
            },
        ]
        
        # Sample data - Bikes
        bikes = [
            {
                'brand': 'Bajaj',
                'model': 'Pulsar 150',
                'year': 2023,
                'category': 'BIKE',
                'front_size': '80/100-17',
                'rear_size': '100/90-17',
                'front_pressure': '25 PSI',
                'rear_pressure': '33 PSI'
            },
            {
                'brand': 'TVS',
                'model': 'Apache RTR 160',
                'year': 2023,
                'category': 'BIKE',
                'front_size': '90/90-17',
                'rear_size': '130/70-17',
                'front_pressure': '25 PSI',
                'rear_pressure': '29 PSI'
            },
            {
                'brand': 'Hero',
                'model': 'Splendor Plus',
                'year': 2023,
                'category': 'BIKE',
                'front_size': '80/100-18',
                'rear_size': '80/100-18',
                'front_pressure': '25 PSI',
                'rear_pressure': '36 PSI'
            },
            {
                'brand': 'Royal Enfield',
                'model': 'Classic 350',
                'year': 2023,
                'category': 'BIKE',
                'front_size': '100/90-19',
                'rear_size': '120/80-18',
                'front_pressure': '22 PSI',
                'rear_pressure': '32 PSI'
            },
        ]
        
        # Sample data - Cars
        cars = [
            {
                'brand': 'Maruti Suzuki',
                'model': 'Swift',
                'year': 2023,
                'category': 'CAR',
                'front_size': '185/65R15',
                'rear_size': '185/65R15',
                'front_pressure': '32 PSI',
                'rear_pressure': '32 PSI'
            },
            {
                'brand': 'Hyundai',
                'model': 'i20',
                'year': 2023,
                'category': 'CAR',
                'front_size': '195/55R16',
                'rear_size': '195/55R16',
                'front_pressure': '33 PSI',
                'rear_pressure': '33 PSI'
            },
            {
                'brand': 'Tata',
                'model': 'Nexon',
                'year': 2023,
                'category': 'CAR',
                'front_size': '215/60R16',
                'rear_size': '215/60R16',
                'front_pressure': '32 PSI',
                'rear_pressure': '32 PSI'
            },
            {
                'brand': 'Mahindra',
                'model': 'Scorpio',
                'year': 2023,
                'category': 'CAR',
                'front_size': '235/65R17',
                'rear_size': '235/65R17',
                'front_pressure': '30 PSI',
                'rear_pressure': '30 PSI'
            },
        ]
        
        # Combine all vehicles
        all_vehicles = scooters + bikes + cars
        
        for vehicle_data in all_vehicles:
            # Create vehicle
            vehicle = Vehicle.objects.create(
                brand=vehicle_data['brand'],
                model=vehicle_data['model'],
                year=vehicle_data['year'],
                category=vehicle_data['category']
            )
            
            # Create tyre size
            tyre_size = TyreSize.objects.create(
                vehicle=vehicle,
                front_size=vehicle_data.get('front_size', ''),
                rear_size=vehicle_data.get('rear_size', ''),
                tyre_size=vehicle_data.get('tyre_size', ''),
                front_pressure=vehicle_data.get('front_pressure', ''),
                rear_pressure=vehicle_data.get('rear_pressure', '')
            )
            
            # Parse detailed dimensions if available
            if 'front_size' in vehicle_data and '/' in vehicle_data['front_size']:
                try:
                    parts = vehicle_data['front_size'].split('/')
                    if len(parts) >= 2:
                        tyre_size.front_width = int(parts[0])
                        second_part = parts[1]
                        if '-' in second_part:
                            aspect_ratio, rim = second_part.split('-')
                            tyre_size.front_aspect_ratio = int(aspect_ratio)
                            tyre_size.front_rim = int(rim.replace('R', '').replace('r', ''))
                except:
                    pass
            
            if 'rear_size' in vehicle_data and '/' in vehicle_data['rear_size']:
                try:
                    parts = vehicle_data['rear_size'].split('/')
                    if len(parts) >= 2:
                        tyre_size.rear_width = int(parts[0])
                        second_part = parts[1]
                        if '-' in second_part:
                            aspect_ratio, rim = second_part.split('-')
                            tyre_size.rear_aspect_ratio = int(aspect_ratio)
                            tyre_size.rear_rim = int(rim.replace('R', '').replace('r', ''))
                except:
                    pass
            
            tyre_size.save()
            
            self.stdout.write(f'Added: {vehicle.brand} {vehicle.model} ({vehicle.year})')
        
        self.stdout.write(self.style.SUCCESS('Successfully added sample data!'))