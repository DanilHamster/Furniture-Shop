import pytest
from django.urls import reverse
from account.models import Cart, CartItem, Buy, LastBuyItem
from service.models import Item, ItemClass, Color
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="user", password="pass")


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(
        username="admin", password="pass", email="admin@example.com"
    )


@pytest.fixture
def item_class(db):
    return ItemClass.objects.create(name="Furniture")


@pytest.fixture
def color(db):
    return Color.objects.create(color="Red")


@pytest.fixture
def item(db, item_class, color):
    return Item.objects.create(
        name="Chair", price=100, count=5, color=color, item_class=item_class
    )


@pytest.fixture
def cart(db, user):
    return Cart.objects.get_or_create(user=user)[0]


@pytest.fixture
def cart_item(db, cart, item):
    return CartItem.objects.create(cart=cart, item=item, quantity=1)


@pytest.mark.django_db
def test_add_to_cart_view(client, user, item):
    client.force_login(user)
    response = client.post(reverse("accounts:add-to-cart"), data={"item_id": item.pk})
    assert response.status_code == 302
    assert CartItem.objects.filter(item=item, cart__user=user).exists()


@pytest.mark.django_db
def test_cart_account_detail_view(client, user, cart):
    client.force_login(user)
    response = client.get(reverse("accounts:cart-acc", kwargs={"pk": cart.pk}))
    assert response.status_code == 200
    assert "cart" in response.context_data


@pytest.mark.django_db
def test_cart_item_update_view(client, user, cart_item):
    client.force_login(user)
    url = reverse("accounts:cart-item", kwargs={"pk": cart_item.pk})
    response = client.post(url, data={"quantity": 2})
    assert response.status_code == 302
    cart_item.refresh_from_db()
    assert cart_item.quantity == 2


@pytest.mark.django_db
def test_cart_item_delete_view(client, user, cart_item):
    client.force_login(user)
    url = reverse("accounts:del-item", kwargs={"pk": cart_item.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert not CartItem.objects.filter(pk=cart_item.pk).exists()


@pytest.mark.django_db
def test_buy_form_creates_buy_and_clears_cart(client, user, item, cart):
    CartItem.objects.create(cart=cart, item=item, quantity=2)
    client.force_login(user)
    response = client.post(
        reverse("accounts:buy-form"),
        data={
            "phone_number": "+380666666666",
            "card_number": "1234123412341234",
            "cvv": "123",
        },
    )
    assert response.status_code == 302
    assert Buy.objects.count() == 1
    assert CartItem.objects.count() == 0
    assert LastBuyItem.objects.count() == 1


@pytest.mark.django_db
def test_profile_view(client, user):
    client.force_login(user)
    response = client.get(reverse("accounts:account-profile"))
    assert response.status_code == 200
    assert response.context_data["user"] == user
