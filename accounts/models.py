# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from cloudinary.models import CloudinaryField


# -------------------------------
# Custom User Manager
# -------------------------------
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

    # accounts/models.py
def user_profile_image_path(instance, filename):
    return f"profiles/{filename}"

# -------------------------------
# Custom User Model
# -------------------------------
class User(AbstractUser):
    username = None  # আমরা username ব্যবহার করব না
    email = models.EmailField(unique=True)

    # ✅ নতুন যোগ করা ফিল্ড
    full_name = models.CharField(max_length=200, blank=True, null=True)

    phone = models.CharField(max_length=20, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    thana = models.CharField(max_length=100, blank=True, null=True)
    village = models.CharField(max_length=150, blank=True, null=True)
    holding_no = models.CharField(max_length=100, blank=True, null=True)
    profile_image = CloudinaryField('profiles', null=True, blank=True)

    bio = models.TextField(blank=True, null=True)

    is_customer = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
