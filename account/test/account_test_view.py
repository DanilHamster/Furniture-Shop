import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from account.forms import (
    CustomUserCreationForm,
    CartItemForm,
    BuyForm,
    UserProfileUpdateForm,
)
from account.models import User, CartItem
from service.models import Item, ItemClass, Color


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="hamster", password="securepass", email="hamster@example.com"
    )


@pytest.fixture
def item_class(db):
    return ItemClass.objects.create(name="Electronics")


@pytest.fixture
def color(db):
    return Color.objects.create(color="Black")


@pytest.fixture
def item(db, item_class, color):
    return Item.objects.create(
        name="Phone", price=999.99, count=5, item_class=item_class, color=color
    )


@pytest.fixture
def cart_item(db, user, item):
    return CartItem.objects.create(cart=user.cart, item=item, quantity=1)


@pytest.mark.django_db
def test_custom_user_creation_form_valid():
    form = CustomUserCreationForm(
        data={
            "username": "newuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "email": "newuser@example.com",
        }
    )
    assert form.is_valid()
    user = form.save()
    assert user.email == "newuser@example.com"


@pytest.mark.django_db
def test_cart_item_form_valid(cart_item):
    form = CartItemForm(instance=cart_item, data={"quantity": 2})
    assert form.is_valid()
    assert form.cleaned_data["quantity"] == 2


@pytest.mark.django_db
def test_cart_item_form_invalid_quantity(cart_item):
    form = CartItemForm(instance=cart_item, data={"quantity": 99})
    assert not form.is_valid()
    assert "quantity" in form.errors


def test_buy_form_valid():
    form = BuyForm(
        data={
            "phone_number": "+380931234567",
            "card_number": "1234567812345678",
            "cvv": "123",
        }
    )
    assert form.is_valid()


def test_buy_form_invalid_phone():
    form = BuyForm(
        data={
            "phone_number": "0931234567",
            "card_number": "1234567812345678",
            "cvv": "123",
        }
    )
    assert not form.is_valid()
    assert "phone_number" in form.errors


def test_buy_form_invalid_card():
    form = BuyForm(
        data={
            "phone_number": "+380931234567",
            "card_number": "abcd1234abcd5678",
            "cvv": "123",
        }
    )
    assert not form.is_valid()
    assert "card_number" in form.errors


@pytest.mark.django_db
def test_user_profile_update_form_valid(user):
    form = UserProfileUpdateForm(
        instance=user,
        data={"first_name": "ham", "last_name": "ster", "email": "hamster@example.com"},
    )
    assert form.is_valid()
    cleaned = form.cleaned_data
    assert cleaned["first_name"] == "Ham"
    assert cleaned["last_name"] == "Ster"


@pytest.mark.django_db
def test_user_profile_update_form_duplicate_email(user):
    User.objects.create_user(
        username="other", email="used@example.com", password="pass"
    )
    form = UserProfileUpdateForm(
        instance=user,
        data={"first_name": "Test", "last_name": "User", "email": "used@example.com"},
    )
    assert not form.is_valid()
    assert "email" in form.errors


def test_user_profile_update_form_avatar_too_large(user):
    big_avatar = SimpleUploadedFile(
        "avatar.jpg", b"x" * (5 * 1024 * 1024), content_type="image/jpeg"
    )
    form = UserProfileUpdateForm(
        instance=user,
        data={"first_name": "Test", "last_name": "User", "email": "test@example.com"},
        files={"avatar": big_avatar},
    )
    assert not form.is_valid()
    assert "avatar" in form.errors
