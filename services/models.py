# services/models.py
from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

def service_image_path(instance, filename):
    """Store service images in a folder named by service id"""
    return f"services/service_{instance.id}/{filename}"


class ServiceCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name


class Service(models.Model):
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="services"
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # ✅ duration in hours
    duration_hours = models.PositiveIntegerField(default=1)

    district = models.CharField(max_length=120, blank=True, null=True)
    thana = models.CharField(max_length=120, blank=True, null=True)
    village = models.CharField(max_length=200, blank=True, null=True)

    image = CloudinaryField('Service_image', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def provider_rating(self):
        """Return average rating from related Review model (if exists)"""
        reviews = self.reviews.all()
        if not reviews.exists():
            return None
        avg = reviews.aggregate(models.Avg("rating"))["rating__avg"]
        return round(avg, 2)

    def location_display(self):
        """Helper: return combined location string"""
        parts = [self.district, self.thana, self.village]
        return ", ".join([p for p in parts if p])
