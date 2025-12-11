import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from tyres.models import Vehicle, TyreSize

class Command(BaseCommand):
    help = 'Import 100+ vehicles from CSV file'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')
    
    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            skipped = 0
            
            for row in reader:
                try:
                    # Check if vehicle already exists
                    slug = slugify(f"{row['brand']} {row['model']} {row['year']}")
                    
                    if Vehicle.objects.filter(slug=slug).exists():
                        self.stdout.write(f"Skipping existing: {row['brand']} {row['model']}")
                        skipped += 1
                        continue
                    
                    # Create vehicle
                    vehicle = Vehicle.objects.create(
                        brand=row['brand'],
                        model=row['model'],
                        year=int(row['year']),
                        category=row['category'],
                        slug=slug
                    )
                    
                    # Create tyre size
                    TyreSize.objects.create(
                        vehicle=vehicle,
                        front_size=row.get('front_size', ''),
                        rear_size=row.get('rear_size', ''),
                        tyre_size=row.get('tyre_size', ''),
                        front_pressure=row.get('front_pressure', ''),
                        rear_pressure=row.get('rear_pressure', ''),
                    )
                    
                    count += 1
                    self.stdout.write(f"Added: {row['brand']} {row['model']} ({row['year']})")
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error adding {row['brand']} {row['model']}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Successfully imported {count} vehicles"))
        if skipped > 0:
            self.stdout.write(f"⏭️ Skipped {skipped} existing vehicles")
        
        # Display summary
        total = Vehicle.objects.count()
        cars = Vehicle.objects.filter(category='CAR').count()
        bikes = Vehicle.objects.filter(category='BIKE').count()
        scooters = Vehicle.objects.filter(category='SCOOTER').count()
        
        self.stdout.write("\n📊 Database Summary:")
        self.stdout.write(f"   Total Vehicles: {total}")
        self.stdout.write(f"   Cars: {cars}")
        self.stdout.write(f"   Bikes: {bikes}")
        self.stdout.write(f"   Scooters: {scooters}")