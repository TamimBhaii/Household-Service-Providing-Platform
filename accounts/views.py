# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.core.mail import EmailMultiAlternatives 

from .forms import (
    CustomerSignUpForm,
    ProviderSignUpForm,
    UserLoginForm,
    EditProfileForm,
    CustomPasswordChangeForm,
)
from bookings.models import Booking

User = get_user_model()

def send_activation_email(request, user):
    subject = "Activate your account - Household Service Platform"
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activate_url = request.build_absolute_uri(
        reverse("accounts:activate", kwargs={"uidb64": uid, "token": token})
    )
    html_message = render_to_string(
        "accounts/email/activation_email.html",
        {"user": user, "activate_url": activate_url},
    )


    text_message = f"Hello {user.email},\nPlease activate your account: {activate_url}"

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=None, 
        to=[user.email],
    )
    email.attach_alternative(html_message, "text/html")
    email.send()


def customer_signup(request):
    if request.method == "POST":
        form = CustomerSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            send_activation_email(request, user)
            messages.success(
                request,
                "✅ Your account has been created successfully. Please check your email and activate your account."
            )
            return redirect("home")
    else:
        form = CustomerSignUpForm()
    return render(request, "accounts/signup_customer.html", {"form": form})


def provider_signup(request):
    if request.method == "POST":
        form = ProviderSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            send_activation_email(request, user)
            messages.success(
                request,
                "✅ Your account has been created successfully. Please check your email and activate your account."
            )
            return redirect("home")
    else:
        form = ProviderSignUpForm()
    return render(request, "accounts/signup_provider.html", {"form": form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated. You can now login.")
        return redirect("accounts:login")
    else:
        return HttpResponse("Activation link is invalid!", status=400)


def user_login(request):
    role = request.GET.get("role", "customer") 
    template = (
        "accounts/customer_login.html"
        if role == "customer"
        else "accounts/provider_login.html"
    )

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("accounts:dashboard")
                else:
                    messages.error(request, "❌ Your account is not activated. Please check your email.")
            else:
                messages.error(request, "❌ Invalid email or password. Please try again.")
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = UserLoginForm()

    return render(request, template, {"form": form})


def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    user = request.user
    if user.is_customer:
        bookings = Booking.objects.filter(customer=user).order_by("-created_at")
        return render(
            request, "accounts/customer_dashboard.html", {"bookings": bookings}
        )
    elif user.is_provider:
        bookings = Booking.objects.filter(provider=user).order_by("-created_at")
        return render(
            request, "accounts/provider_dashboard.html", {"bookings": bookings}
        )
    return redirect("home")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated")
            return redirect("accounts:dashboard")
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required
def my_bookings(request):
    if request.user.is_customer:
        bookings = Booking.objects.filter(customer=request.user).order_by("-created_at")
    elif request.user.is_provider:
        bookings = Booking.objects.filter(provider=request.user).order_by("-created_at")
    else:
        bookings = []
    return render(request, "accounts/my_bookings.html", {"bookings": bookings})


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:password_change_done")
