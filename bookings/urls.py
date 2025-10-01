from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("create/<int:service_id>/", views.create_booking, name="create_booking"),
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("update/<int:booking_id>/<str:status>/", views.update_status, name="update_status"),
    path("status/", views.booking_status, name="booking_status"),
    path("provider/requests/", views.provider_requests, name="provider_requests"),
]
