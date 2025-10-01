# reviews/models.py
from django.db import models
from django.conf import settings
from services.models import Service

class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="reviews")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)  # 1–5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("service", "customer")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.rating}★ by {self.customer.email} for {self.service.title}"
