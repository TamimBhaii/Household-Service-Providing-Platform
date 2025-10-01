# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Booking
from services.models import Service
from reviews.models import Review 


@login_required
def create_booking(request, service_id):
    """Customer creates a booking request for a service"""
    service = get_object_or_404(Service, id=service_id)

    if request.method == "POST":
        Booking.objects.create(
            service=service,
            customer=request.user,
            provider=service.provider,
            requested_datetime=timezone.now(),
            customer_name=request.user.full_name or request.user.email,
            customer_phone=request.user.phone,
            customer_district=request.user.district,
            customer_thana=request.user.thana,
            customer_village=request.user.village,
            customer_holding_no=request.user.holding_no,
            note=request.POST.get("note", "")
        )
        messages.success(request, "Booking request sent successfully.")
        return redirect("accounts:dashboard")

    return render(request, "bookings/create_booking.html", {"service": service})


@login_required
def cancel_booking(request, booking_id):
    """Customer can cancel only pending bookings"""
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if booking.status == "pending":
        booking.status = "cancelled"
        booking.save()
        messages.success(request, "Booking cancelled.")
    else:
        messages.error(request, "Only pending bookings can be cancelled.")
    return redirect("accounts:dashboard")


@login_required
@require_POST
def update_status(request, booking_id, status):
    """Provider can update status of a booking"""
    booking = get_object_or_404(Booking, id=booking_id, provider=request.user)
    if status in ["accepted", "rejected", "completed"]:
        booking.status = status
        booking.save()
        messages.success(request, f"Booking marked as {status}.")
    else:
        messages.error(request, "Invalid status.")
    return redirect("bookings:provider_requests")
@login_required
def booking_status(request):
    """Show all booking status for the logged in customer"""
    if not request.user.is_customer:
        return redirect("accounts:dashboard")

    bookings = Booking.objects.filter(customer=request.user).order_by("-created_at")
    for b in bookings:
        b.already_reviewed = Review.objects.filter(service=b.service, customer=request.user).exists()

    return render(request, "bookings/status.html", {"bookings": bookings})

@login_required
def provider_requests(request):
    """Show all hire requests for the logged in provider"""
    if not request.user.is_provider:
        return redirect("accounts:dashboard")

    bookings = Booking.objects.filter(provider=request.user).order_by("-created_at")
    return render(request, "bookings/provider_requests.html", {"bookings": bookings})
