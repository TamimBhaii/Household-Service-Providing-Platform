# services/admin.py
from django.contrib import admin
from .models import ServiceCategory, Service

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "provider", "category", "price", "district", "created_at")
    search_fields = ("title", "provider__email", "district", "thana", "village")
    list_filter = ("category", "district")
