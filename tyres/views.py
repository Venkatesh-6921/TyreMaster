# tyres/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Vehicle, TyreSize , VehicleSubmission
from .forms import VehicleSubmissionForm
from django.contrib import messages
from django.shortcuts import render, redirect 
from django.contrib import admin
from django.utils import timezone

def home(request):
    """Homepage with search"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    vehicles = Vehicle.objects.all()
    
    # Apply filters if provided
    if query:
        vehicles = vehicles.filter(
            Q(brand__icontains=query) | 
            Q(model__icontains=query) |
            Q(year__icontains=query)
        )
    
    if category:
        vehicles = vehicles.filter(category=category)
    
    # Get distinct brands for filter
    brands = Vehicle.objects.values_list('brand', flat=True).distinct().order_by('brand')
    
    context = {
        'vehicles': vehicles[:20],  # Limit to 20 results
        'query': query,
        'category': category,
        'brands': brands,
        'categories': Vehicle.CATEGORY_CHOICES,
    }
    return render(request, 'tyres/home.html', context)

def vehicle_list(request):
    """List all vehicles with advanced filters"""
    # Get filter parameters
    category = request.GET.get('category', '')
    brand = request.GET.get('brand', '')
    year_from = request.GET.get('year_from', '')
    year_to = request.GET.get('year_to', '')
    tyre_width = request.GET.get('tyre_width', '')
    rim_size = request.GET.get('rim_size', '')
    sort_by = request.GET.get('sort_by', 'brand')
    
    vehicles = Vehicle.objects.all()
    
    # Apply filters
    if category:
        vehicles = vehicles.filter(category=category)
    
    if brand:
        vehicles = vehicles.filter(brand=brand)
    
    if year_from:
        vehicles = vehicles.filter(year__gte=year_from)
    
    if year_to:
        vehicles = vehicles.filter(year__lte=year_to)
    
    # Filter by tyre characteristics
    if tyre_width or rim_size:
        # Get tyre sizes matching criteria
        tyre_filter = Q()
        
        if tyre_width:
            # Convert to integer for range filtering
            try:
                width = int(tyre_width)
                tyre_filter |= Q(front_width=width) | Q(rear_width=width)
            except:
                pass
        
        if rim_size:
            try:
                rim = int(rim_size)
                tyre_filter |= Q(front_rim=rim) | Q(rear_rim=rim)
            except:
                pass
        
        # Get vehicle IDs with matching tyre sizes
        matching_tyres = TyreSize.objects.filter(tyre_filter)
        vehicle_ids = matching_tyres.values_list('vehicle_id', flat=True)
        vehicles = vehicles.filter(id__in=vehicle_ids)
    
    # Apply sorting
    if sort_by == 'year_asc':
        vehicles = vehicles.order_by('year')
    elif sort_by == 'year_desc':
        vehicles = vehicles.order_by('-year')
    elif sort_by == 'model':
        vehicles = vehicles.order_by('model')
    else:  # brand (default)
        vehicles = vehicles.order_by('brand', 'model')
    
    # Get distinct values for filter dropdowns
    brands = Vehicle.objects.values_list('brand', flat=True).distinct().order_by('brand')
    years = Vehicle.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    # Get tyre width and rim size ranges
    tyre_widths = TyreSize.objects.exclude(
        Q(front_width__isnull=True) & Q(rear_width__isnull=True)
    ).values_list('front_width', 'rear_width').distinct()
    
    rim_sizes = TyreSize.objects.exclude(
        Q(front_rim__isnull=True) & Q(rear_rim__isnull=True)
    ).values_list('front_rim', 'rear_rim').distinct()
    
    # Flatten and get unique values
    width_list = set()
    for fw, rw in tyre_widths:
        if fw: width_list.add(fw)
        if rw: width_list.add(rw)
    
    rim_list = set()
    for fr, rr in rim_sizes:
        if fr: rim_list.add(fr)
        if rr: rim_list.add(rr)
    
    context = {
        'vehicles': vehicles,
        'brands': brands,
        'categories': Vehicle.CATEGORY_CHOICES,
        'years': years,
        'tyre_widths': sorted(width_list),
        'rim_sizes': sorted(rim_list),
        'selected_category': category,
        'selected_brand': brand,
        'selected_year_from': year_from,
        'selected_year_to': year_to,
        'selected_tyre_width': tyre_width,
        'selected_rim_size': rim_size,
        'selected_sort': sort_by,
    }
    return render(request, 'tyres/vehicle_list.html', context)

def vehicle_detail(request, slug):
    """Vehicle detail page"""
    vehicle = get_object_or_404(Vehicle, slug=slug)
    
    # Get similar vehicles (same brand or category)
    similar_vehicles = Vehicle.objects.filter(
        Q(brand=vehicle.brand) | Q(category=vehicle.category)
    ).exclude(id=vehicle.id)[:5]
    
    context = {
        'vehicle': vehicle,
        'similar_vehicles': similar_vehicles,
    }
    return render(request, 'tyres/vehicle_detail.html', context)

def about(request):
    """About page"""
    return render(request, 'tyres/about.html')

def search_by_tyre(request):
    """Search vehicles by tyre size"""
    front_size = request.GET.get('front', '')
    rear_size = request.GET.get('rear', '')
    
    results = []
    
    if front_size or rear_size:
        tyre_sizes = TyreSize.objects.all()
        
        if front_size:
            tyre_sizes = tyre_sizes.filter(
                Q(front_size__icontains=front_size) |
                Q(tyre_size__icontains=front_size)
            )
        
        if rear_size:
            tyre_sizes = tyre_sizes.filter(
                Q(rear_size__icontains=rear_size) |
                Q(tyre_size__icontains=rear_size)
            )
        
        results = [ts.vehicle for ts in tyre_sizes]
    
    context = {
        'results': results,
        'front_size': front_size,
        'rear_size': rear_size,
    }
    return render(request, 'tyres/search_by_tyre.html', context)

def submit_vehicle(request):
    """Handle user submissions for missing vehicles"""
    if request.method == 'POST':
        form = VehicleSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            
            # Send email notification (optional)
            send_submission_email(submission)
            
            messages.success(request, 
                f'Thank you! Your submission for {submission.brand} {submission.model} has been received. '
                'We will review it and add it to our database soon.')
            return redirect('submission_success')
    else:
        form = VehicleSubmissionForm()
    
    return render(request, 'tyres/submit_vehicle.html', {'form': form})

def submission_success(request):
    return render(request, 'tyres/submission_success.html')

def send_submission_email(submission):
    """Send email notification about new submission"""
    # This is a placeholder - configure email backend in settings.py
    pass

# Add admin view for submissions
@admin.register(VehicleSubmission)
class VehicleSubmissionAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'status', 'user_name', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['brand', 'model', 'user_name', 'user_email']
    actions = ['approve_submissions', 'reject_submissions']
    
    def approve_submissions(self, request, queryset):
        for submission in queryset:
            # Create actual vehicle from submission
            vehicle = Vehicle.objects.create(
                brand=submission.brand,
                model=submission.model,
                year=submission.year,
                category=submission.category
            )
            
            TyreSize.objects.create(
                vehicle=vehicle,
                front_size=submission.front_size,
                rear_size=submission.rear_size,
                tyre_size=submission.tyre_size,
                front_pressure=submission.front_pressure,
                rear_pressure=submission.rear_pressure
            )
            
            submission.status = 'APPROVED'
            submission.admin_notes = f'Approved and added to database on {timezone.now().date()}'
            submission.save()
        
        self.message_user(request, f"{queryset.count()} submissions approved and added to database.")
    
    approve_submissions.short_description = "Approve selected submissions"
    
    def reject_submissions(self, request, queryset):
        queryset.update(status='REJECTED')
        self.message_user(request, f"{queryset.count()} submissions rejected.")

# tyres/views.py - Add calculator functions
import math
from django.http import JsonResponse

def tyre_calculator(request):
    """Tyre calculator main page"""
    return render(request, 'tyres/tyre_calculator.html')

def calculate_tyre_size(request):
    """API endpoint for tyre calculations"""
    if request.method == 'POST':
        data = request.POST
        
        # Get input values
        width = int(data.get('width', 0))
        aspect_ratio = int(data.get('aspect_ratio', 0))
        rim_diameter = int(data.get('rim_diameter', 0))
        
        # Calculate tyre diameter in mm
        sidewall_height = width * (aspect_ratio / 100)
        tyre_diameter_mm = (rim_diameter * 25.4) + (2 * sidewall_height)
        
        # Calculate circumference
        circumference_mm = math.pi * tyre_diameter_mm
        circumference_in = circumference_mm / 25.4
        
        # Calculate revolutions per km/mile
        revs_per_km = 1000000 / circumference_mm
        revs_per_mile = 1609344 / circumference_mm
        
        # Alternative sizes (plus/minus 10mm width, 5% aspect ratio)
        alt_sizes = []
        width_variations = [-20, -10, 10, 20]
        ratio_variations = [-10, -5, 5, 10]
        
        for w_var in width_variations:
            for r_var in ratio_variations:
                new_width = width + w_var
                new_ratio = aspect_ratio + r_var
                
                if new_width > 0 and new_ratio > 0:
                    new_sidewall = new_width * (new_ratio / 100)
                    new_diameter = (rim_diameter * 25.4) + (2 * new_sidewall)
                    diameter_diff = ((new_diameter - tyre_diameter_mm) / tyre_diameter_mm) * 100
                    
                    # Only include reasonable alternatives (±3% diameter difference)
                    if abs(diameter_diff) <= 3:
                        alt_sizes.append({
                            'size': f"{new_width}/{new_ratio}R{rim_diameter}",
                            'width': new_width,
                            'aspect_ratio': new_ratio,
                            'diameter_diff': round(diameter_diff, 1),
                            'speedo_error': f"{'+' if diameter_diff > 0 else ''}{round(diameter_diff, 1)}%"
                        })
        
        # Convert to imperial size
        width_inches = width / 25.4
        imperial_size = f"{round(width_inches, 1)}-{rim_diameter}"
        
        response_data = {
            'metric_size': f"{width}/{aspect_ratio}R{rim_diameter}",
            'imperial_size': imperial_size,
            'diameter_mm': round(tyre_diameter_mm, 1),
            'diameter_inches': round(tyre_diameter_mm / 25.4, 1),
            'circumference_mm': round(circumference_mm, 1),
            'circumference_inches': round(circumference_in, 1),
            'sidewall_height': round(sidewall_height, 1),
            'revolutions_per_km': round(revs_per_km, 1),
            'revolutions_per_mile': round(revs_per_mile, 1),
            'alternative_sizes': alt_sizes[:6],  # Limit to 6 alternatives
        }
        
        return JsonResponse(response_data)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def compare_tyres(request):
    """Compare two tyre sizes"""
    return render(request, 'tyres/compare_tyres.html')



def search_by_size_range(request):
    """Search vehicles by tyre size range"""
    min_width = request.GET.get('min_width', '')
    max_width = request.GET.get('max_width', '')
    min_rim = request.GET.get('min_rim', '')
    max_rim = request.GET.get('max_rim', '')
    
    vehicles = Vehicle.objects.all()
    tyre_filter = Q()
    
    if min_width or max_width:
        # Filter by tyre width range
        if min_width:
            try:
                min_w = int(min_width)
                tyre_filter &= (Q(front_width__gte=min_w) | Q(rear_width__gte=min_w))
            except:
                pass
        
        if max_width:
            try:
                max_w = int(max_width)
                tyre_filter &= (Q(front_width__lte=max_w) | Q(rear_width__lte=max_w))
            except:
                pass
    
    if min_rim or max_rim:
        # Filter by rim size range
        rim_filter = Q()
        
        if min_rim:
            try:
                min_r = int(min_rim)
                rim_filter |= (Q(front_rim__gte=min_r) | Q(rear_rim__gte=min_r))
            except:
                pass
        
        if max_rim:
            try:
                max_r = int(max_rim)
                rim_filter |= (Q(front_rim__lte=max_r) | Q(rear_rim__lte=max_r))
            except:
                pass
        
        tyre_filter &= rim_filter
    
    # Get vehicle IDs with matching tyre sizes
    if tyre_filter:
        matching_tyres = TyreSize.objects.filter(tyre_filter)
        vehicle_ids = matching_tyres.values_list('vehicle_id', flat=True)
        vehicles = vehicles.filter(id__in=vehicle_ids)
    
    context = {
        'vehicles': vehicles,
        'min_width': min_width,
        'max_width': max_width,
        'min_rim': min_rim,
        'max_rim': max_rim,
    }
    
    return render(request, 'tyres/size_range_search.html', context)

def pressure_chart(request, slug):
    """Show tyre pressure chart for vehicle"""
    vehicle = get_object_or_404(Vehicle, slug=slug)
    
    # Check if vehicle has tyre data
    if not hasattr(vehicle, 'tyres'):
        return render(request, 'tyres/no_pressure_data.html', {'vehicle': vehicle})
    
    # Get pressure data (in real app, this would come from database)
    # For now, we'll create sample data
    pressure_data = {
        'cold_front': vehicle.tyres.front_pressure or '29',
        'cold_rear': vehicle.tyres.rear_pressure or '33',
        'hot_front': '32',  # In real app, these would be in database
        'hot_rear': '36',
        'loaded_front': '31',
        'loaded_rear': '35',
        'max_front': '36',
        'max_rear': '40',
    }
    
    context = {
        'vehicle': vehicle,
        'pressure_data': pressure_data,
    }
    
    return render(request, 'tyres/pressure_chart.html', context)

