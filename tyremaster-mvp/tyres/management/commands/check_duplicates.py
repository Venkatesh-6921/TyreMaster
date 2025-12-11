
import csv
from django.core.management.base import BaseCommand
from tyres.models import Vehicle

class Command(BaseCommand):
    help = 'Check for duplicates in CSV before importing'
    
    def handle(self, *args, **options):
        csv_file = 'additional_vehicles.csv'
        duplicates = []
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                brand = row['brand'].strip()
                model = row['model'].strip()
                year = int(row['year'])
                
                # Check if exists
                exists = Vehicle.objects.filter(
                    brand__iexact=brand,
                    model__iexact=model,
                    year=year
                ).exists()
                
                if exists:
                    duplicates.append(f"{brand} {model} ({year})")
        
        if duplicates:
            self.stdout.write(self.style.WARNING(f"Found {len(duplicates)} duplicates:"))
            for dup in duplicates:
                self.stdout.write(f"  - {dup}")
        else:
            self.stdout.write(self.style.SUCCESS("No duplicates found! Safe to import."))