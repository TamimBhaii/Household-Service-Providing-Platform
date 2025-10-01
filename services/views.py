# services/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg   # ✅ added

from .models import Service, ServiceCategory
from .forms import ServiceForm


def service_list(request):
    """All available services (with search) for customers."""
    q = request.GET.get("q", "")
    services = Service.objects.all().order_by("-created_at")
    if q:
        services = services.filter(title__icontains=q)

    return render(request, "services/service_list.html", {
        "services": services,
        "q": q,
    })


def service_detail(request, pk):
    """Service details page with provider info + average rating."""
    service = get_object_or_404(Service, pk=pk)
    provider = service.provider
    rating = service.provider_rating()

    # ✅ calculate avg rating for provider
    avg_rating = service.reviews.aggregate(Avg("rating"))["rating__avg"] or 0
    avg_rating = round(avg_rating, 1) if avg_rating else None

    return render(request, "services/service_detail.html", {
        "service": service,
        "provider": provider,
        "rating": rating,
        "avg_rating": avg_rating,   # ✅ passed to template
    })


@login_required
def add_service(request):
    """Providers can add new services."""
    if not request.user.is_provider:
        messages.error(request, "Only providers can add services.")
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            messages.success(request, "Service added successfully.")
            return redirect("services:my_services")
    else:
        form = ServiceForm()

    return render(request, "services/add_service.html", {"form": form})


@login_required
def my_services(request):
    """Provider can see only his own services."""
    if not request.user.is_provider:
        messages.error(request, "Only providers can view this page.")
        return redirect("accounts:dashboard")

    services = Service.objects.filter(provider=request.user).order_by("-created_at")
    return render(request, "services/my_services.html", {"services": services})




@login_required
def edit_service(request, pk):
    """Providers can edit their own services"""
    service = get_object_or_404(Service, pk=pk, provider=request.user)

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully ✅")
            return redirect("services:my_services")
    else:
        form = ServiceForm(instance=service)

    return render(request, "services/edit_service.html", {"form": form, "service": service})


@login_required
def delete_service(request, pk):
    """Providers can delete their own services"""
    service = get_object_or_404(Service, pk=pk, provider=request.user)

    if request.method == "POST":
        service.delete()
        messages.success(request, "Service deleted successfully 🗑️")
        return redirect("services:my_services")

    return render(request, "services/delete_service.html", {"service": service})
