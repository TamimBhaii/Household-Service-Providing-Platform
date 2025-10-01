from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("service", "customer", "rating", "created_at")
    search_fields = ("service__title", "customer__email")
    list_filter = ("rating", "created_at")
