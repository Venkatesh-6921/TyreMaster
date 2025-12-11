# tyres/admin.py
from django.contrib import admin
from .models import Vehicle, TyreSize

class TyreSizeInline(admin.StackedInline):
    model = TyreSize
    can_delete = False
    verbose_name_plural = 'Tyre Sizes'
    fieldsets = (
        ('Front Tyre', {
            'fields': ('front_size', 'front_width', 'front_aspect_ratio', 'front_rim', 'front_pressure')
        }),
        ('Rear Tyre', {
            'fields': ('rear_size', 'rear_width', 'rear_aspect_ratio', 'rear_rim', 'rear_pressure')
        }),
        ('Same Tyres (if applicable)', {
            'fields': ('tyre_size',)
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'category', 'slug']
    list_filter = ['category', 'brand', 'year']
    search_fields = ['brand', 'model']
    prepopulated_fields = {'slug': ('brand', 'model', 'year')}
    inlines = [TyreSizeInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('brand', 'model', 'year', 'category')
        }),
        ('SEO', {
            'fields': ('slug',),
            'classes': ('collapse',)
        }),
    )

@admin.register(TyreSize)
class TyreSizeAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'get_front_display', 'get_rear_display']
    list_filter = ['vehicle__category']
    search_fields = ['vehicle__brand', 'vehicle__model']