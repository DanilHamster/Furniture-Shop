from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.template.defaultfilters import first

from account.models import User, CartItem
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email address")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)


class CartItemForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = CartItem
        fields = ("quantity",)

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        item = self.instance.item
        max_qty = item.count
        name_item = self.instance.item.name
        if quantity > max_qty:
            raise forms.ValidationError(
                f"{name_item} on warehouse: {max_qty}\n"
                f"You can select maximum {max_qty} of {name_item}"
            )
        return quantity


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("avatar", "first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Select correct email.")
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("This email used ")
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            if avatar.size > 4 * 1024 * 1024:
                raise ValidationError("Size of image must be 1024*1024 and  4MB.")
        return avatar

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if first_name:
            return first_name.title()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if last_name:
            return last_name.title()
        return last_name
