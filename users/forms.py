from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username"]


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            # Only superuser can update user password via admin site
            # To implement the reset of passwords via frontend will need
            # require extra views, templates and the setup of a mail server
            # "password",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "latitude",
            "longitude",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
