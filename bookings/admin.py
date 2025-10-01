# bookings/admin.py
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("service", "customer", "provider", "status", "requested_datetime", "created_at")
    list_filter = ("status",)
    search_fields = ("customer__email", "provider__email", "service__title")
