# reviews/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from services.models import Service
from bookings.models import Booking

@login_required
def add_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)


    if booking.status != "accepted":
        messages.error(request, "❌ You can only review after your booking is accepted.")
        return redirect("bookings:booking_status")


    if Review.objects.filter(service=booking.service, customer=request.user).exists():
        messages.warning(request, "⚠ You have already submitted a review for this service.")
        return redirect("bookings:booking_status")

    if request.method == "POST":
        rating = int(request.POST.get("rating", 5))
        comment = request.POST.get("comment", "")

        Review.objects.create(
            service=booking.service,
            customer=request.user,
            rating=rating,
            comment=comment
        )
        messages.success(request, "✅ Review submitted successfully.")
        return redirect("bookings:booking_status")

    return render(request, "reviews/add_review.html", {"booking": booking})
