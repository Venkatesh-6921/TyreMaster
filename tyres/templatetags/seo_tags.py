# tyres/templatetags/seo_tags.py
from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.simple_tag
def vehicle_schema(vehicle):
    """Generate JSON-LD schema for vehicle"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Car",
        "name": f"{vehicle.brand} {vehicle.model}",
        "brand": {
            "@type": "Brand",
            "name": vehicle.brand
        },
        "model": vehicle.model,
        "modelDate": str(vehicle.year),
        "vehicleType": vehicle.get_category_display(),
    }
    
    if hasattr(vehicle, 'tyres'):
        schema["description"] = f"Tyre specifications: Front: {vehicle.tyres.get_front_display()}, Rear: {vehicle.tyres.get_rear_display()}"
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>')