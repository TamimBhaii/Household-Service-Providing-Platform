# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

User = get_user_model()

# shared input classes (Tailwind)
INPUT_CLASSES = (
    "w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md shadow-black/30 "
    "focus:outline-none focus:ring-2 focus:ring-green-500 placeholder-gray-400"
)


class CustomerSignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASSES, "placeholder": "New password"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASSES, "placeholder": "Confirm password"}
        ),
    )

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "phone",
            "district",
            "thana",
            "village",
            "holding_no",
            "profile_image",
            "bio",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Full Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Email"}
            ),
            "phone": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Phone Number"}
            ),
            "district": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "District"}
            ),
            "thana": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Thana"}
            ),
            "village": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Village"}
            ),
            "holding_no": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Holding no"}
            ),
            "profile_image": forms.ClearableFileInput(
                attrs={"class": "w-full text-sm text-gray-600"}
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg shadow-md shadow-black/30",
                    "rows": 3,
                    "placeholder": "Short bio (optional)",
                }
            ),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_customer = True
        user.is_active = False
        if commit:
            user.save()
        return user


class ProviderSignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASSES, "placeholder": "New password"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASSES, "placeholder": "Confirm password"}
        ),
    )

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "phone",
            "district",
            "thana",
            "village",
            "holding_no",
            "profile_image",
            "bio",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Full Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Email"}
            ),
            "phone": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Phone Number"}
            ),
            "district": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "District"}
            ),
            "thana": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Thana"}
            ),
            "village": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Village"}
            ),
            "holding_no": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Holding no"}
            ),
            "profile_image": forms.ClearableFileInput(
                attrs={"class": "w-full text-sm text-gray-600"}
            ),
            "bio": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "Describe your services, experience...",
                }
            ),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_provider = True
        user.is_active = False
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": INPUT_CLASSES, "placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASSES, "placeholder": "Password"}
        )
    )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "full_name",
            "phone",
            "district",
            "thana",
            "village",
            "holding_no",
            "bio",
            "profile_image",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Full Name"}
            ),
            "phone": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "district": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "thana": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "village": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "holding_no": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "bio": forms.Textarea(
                attrs={
                    "class": "w-full px-2 py-2 border rounded-lg shadow-md shadow-black/30",
                    "rows": 2,
                    "placeholder": "Short bio (optional)",
                }
            ),
            "profile_image": forms.ClearableFileInput(
                attrs={"class": "w-full text-sm text-gray-600"}
            ),
        }


# ✅ Tailwind-styled Password Change Form
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASSES, "placeholder": "Current password"}
        )
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASSES, "placeholder": "New password"}
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASSES, "placeholder": "Confirm new password"}
        )
    )
