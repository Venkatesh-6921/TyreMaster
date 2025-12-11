# tyres/models.py
from django.db import models

class Vehicle(models.Model):
    CATEGORY_CHOICES = [
        ('CAR', 'Car'),
        ('BIKE', 'Bike'),
        ('SCOOTER', 'Scooter'),
    ]
    
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    
    # SEO friendly slug
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        ordering = ['brand', 'model', 'year']
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Create slug from brand, model, year
            slug_text = f"{self.brand.lower()}-{self.model.lower()}-{self.year}"
            self.slug = slug_text.replace(' ', '-')
        super().save(*args, **kwargs)

class TyreSize(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='tyres')
    
    # Front tyre
    front_size = models.CharField(max_length=20, blank=True, verbose_name="Front Tyre Size")
    front_width = models.IntegerField(null=True, blank=True, verbose_name="Front Width (mm)")
    front_aspect_ratio = models.IntegerField(null=True, blank=True, verbose_name="Front Aspect Ratio (%)")
    front_rim = models.IntegerField(null=True, blank=True, verbose_name="Front Rim Diameter (inches)")
    front_pressure = models.CharField(max_length=20, blank=True, verbose_name="Front Pressure (PSI)")
    
    # Rear tyre
    rear_size = models.CharField(max_length=20, blank=True, verbose_name="Rear Tyre Size")
    rear_width = models.IntegerField(null=True, blank=True, verbose_name="Rear Width (mm)")
    rear_aspect_ratio = models.IntegerField(null=True, blank=True, verbose_name="Rear Aspect Ratio (%)")
    rear_rim = models.IntegerField(null=True, blank=True, verbose_name="Rear Rim Diameter (inches)")
    rear_pressure = models.CharField(max_length=20, blank=True, verbose_name="Rear Pressure (PSI)")
    
    # For vehicles with same tyres front & rear
    tyre_size = models.CharField(max_length=20, blank=True, verbose_name="Tyre Size (if same)")
    
    notes = models.TextField(blank=True, verbose_name="Additional Notes")
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Tyre sizes for {self.vehicle}"
    
    def get_front_display(self):
        if self.front_size:
            return self.front_size
        elif self.front_width and self.front_aspect_ratio and self.front_rim:
            return f"{self.front_width}/{self.front_aspect_ratio}-{self.front_rim}"
        return "Not specified"
    
    def get_rear_display(self):
        if self.rear_size:
            return self.rear_size
        elif self.rear_width and self.rear_aspect_ratio and self.rear_rim:
            return f"{self.rear_width}/{self.rear_aspect_ratio}-{self.rear_rim}"
        return "Not specified"
    
     # Alternative sizes
    alt_size_1 = models.CharField(max_length=20, blank=True, verbose_name="Alternative Size 1")
    alt_size_2 = models.CharField(max_length=20, blank=True, verbose_name="Alternative Size 2")
    alt_size_3 = models.CharField(max_length=20, blank=True, verbose_name="Alternative Size 3")
    
    # Pressure variations
    pressure_cold_front = models.CharField(max_length=20, blank=True, verbose_name="Cold Front Pressure")
    pressure_cold_rear = models.CharField(max_length=20, blank=True, verbose_name="Cold Rear Pressure")
    pressure_hot_front = models.CharField(max_length=20, blank=True, verbose_name="Hot Front Pressure")
    pressure_hot_rear = models.CharField(max_length=20, blank=True, verbose_name="Hot Rear Pressure")
    pressure_loaded_front = models.CharField(max_length=20, blank=True, verbose_name="Loaded Front Pressure")
    pressure_loaded_rear = models.CharField(max_length=20, blank=True, verbose_name="Loaded Rear Pressure")
    
    # Tyre specifications
    ply_rating = models.CharField(max_length=10, blank=True, verbose_name="Ply Rating")
    load_index = models.CharField(max_length=10, blank=True, verbose_name="Load Index")
    speed_rating = models.CharField(max_length=5, blank=True, verbose_name="Speed Rating")
    tube_type = models.CharField(max_length=20, blank=True, choices=[
        ('TUBE', 'Tube Type'),
        ('TUBELESS', 'Tubeless'),
        ('BOTH', 'Both'),
    ])



class VehicleSubmission(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    # User information
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=15, blank=True)
    
    # Vehicle information
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    category = models.CharField(max_length=10, choices=Vehicle.CATEGORY_CHOICES)
    
    # Tyre information
    front_size = models.CharField(max_length=20, blank=True)
    rear_size = models.CharField(max_length=20, blank=True)
    tyre_size = models.CharField(max_length=20, blank=True)
    front_pressure = models.CharField(max_length=20, blank=True)
    rear_pressure = models.CharField(max_length=20, blank=True)
    
    # Additional info
    source = models.CharField(max_length=200, blank=True, help_text="Where did you get this information?")
    comments = models.TextField(blank=True)
    
    # Admin
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) - {self.status}"
    

class AffiliateLink(models.Model):
    TYPE_CHOICES = [
        ('TYRE', 'Tyre Retailer'),
        ('TOOL', 'Tool Retailer'),
        ('SERVICE', 'Service Center'),
    ]
    
    name = models.CharField(max_length=100)
    link_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    url = models.URLField()
    description = models.TextField(blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_link_type_display()})"
    

class TyrePressureData(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='pressure_data')
    
    # Standard pressures
    standard_front = models.CharField(max_length=10, verbose_name="Standard Front Pressure")
    standard_rear = models.CharField(max_length=10, verbose_name="Standard Rear Pressure")
    
    # Temperature variations
    cold_front = models.CharField(max_length=10, blank=True, verbose_name="Cold Front Pressure")
    cold_rear = models.CharField(max_length=10, blank=True, verbose_name="Cold Rear Pressure")
    hot_front = models.CharField(max_length=10, blank=True, verbose_name="Hot Front Pressure")
    hot_rear = models.CharField(max_length=10, blank=True, verbose_name="Hot Rear Pressure")
    
    # Load variations
    light_load_front = models.CharField(max_length=10, blank=True, verbose_name="Light Load Front")
    light_load_rear = models.CharField(max_length=10, blank=True, verbose_name="Light Load Rear")
    full_load_front = models.CharField(max_length=10, blank=True, verbose_name="Full Load Front")
    full_load_rear = models.CharField(max_length=10, blank=True, verbose_name="Full Load Rear")
    
    # Maximum safe pressures
    max_front = models.CharField(max_length=10, blank=True, verbose_name="Maximum Front Pressure")
    max_rear = models.CharField(max_length=10, blank=True, verbose_name="Maximum Rear Pressure")
    
    # Seasonal adjustments
    summer_adjustment = models.CharField(max_length=10, default="-2 PSI", verbose_name="Summer Adjustment")
    winter_adjustment = models.CharField(max_length=10, default="+2 PSI", verbose_name="Winter Adjustment")
    
    notes = models.TextField(blank=True, verbose_name="Additional Notes")
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Tyre Pressure Data"
        verbose_name_plural = "Tyre Pressure Data"
    
    def __str__(self):
        return f"Pressure data for {self.vehicle}"
    