from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    # Customer creates a booking
    path("create/<int:service_id>/", views.create_booking, name="create_booking"),

    # Customer cancels a booking
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),

    # Provider updates booking status (accept/reject/complete)
    path("update/<int:booking_id>/<str:status>/", views.update_status, name="update_status"),

    # Customer status page
    path("status/", views.booking_status, name="booking_status"),

    # Provider hire requests page
    path("provider/requests/", views.provider_requests, name="provider_requests"),
]
