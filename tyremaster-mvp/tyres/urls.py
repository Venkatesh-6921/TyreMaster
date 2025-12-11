# tyres/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicle/<slug:slug>/', views.vehicle_detail, name='vehicle_detail'),
    path('search-by-tyre/', views.search_by_tyre, name='search_by_tyre'),
    path('about/', views.about, name='about'),
    path('submit-vehicle/', views.submit_vehicle, name='submit_vehicle'),
    path('submission-success/', views.submission_success, name='submission_success'),
    path('tyre-calculator/', views.tyre_calculator, name='tyre_calculator'),
    path('compare-tyres/', views.compare_tyres, name='compare_tyres'),
    path('calculate-tyre-size/', views.calculate_tyre_size, name='calculate_tyre_size'),
    path('search-size-range/', views.search_by_size_range, name='search_by_size_range'),
    path('vehicle/<slug:slug>/pressure-chart/', views.pressure_chart, name='pressure_chart'),
]