# bookings/models.py
from django.db import models
from django.conf import settings
from services.models import Service

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_bookings")
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="provider_bookings")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    requested_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    # snapshot of customer info
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=30)
    customer_district = models.CharField(max_length=120, blank=True, null=True)
    customer_thana = models.CharField(max_length=120, blank=True, null=True)
    customer_village = models.CharField(max_length=200, blank=True, null=True)
    customer_holding_no = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.service.title} - {self.customer.email} ({self.status})"
