import pytest
from account.models import User, Cart, CartItem, Buy, LastBuyItem, Comment
from service.models import Item, ItemClass, Color


# 🔧 Fixtures
@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="hamster", password="securepass", email="hamster@example.com"
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
        name="Chair", price=100, count=5, item_class=item_class, color=color
    )


@pytest.fixture
def cart(db, user):
    return Cart.objects.get_or_create(user=user)[0]


@pytest.fixture
def cart_item(db, cart, item):
    return CartItem.objects.create(cart=cart, item=item, quantity=2)


def test_user_str_and_avatar(user):
    assert user.username == "hamster"
    assert user.get_image_url() == "/static/img/placeholder.png"


def test_cart_str(cart):
    assert str(cart) == f"Cart of {cart.user.username}"


@pytest.mark.django_db
def test_cart_total_price(cart_item):
    cart = cart_item.cart
    total = cart.total_price()
    assert total == cart_item.quantity * cart_item.item.price


def test_cart_item_str(cart_item):
    expected = f"Sum for 2 × Chair: $200.00"
    assert str(cart_item) == expected


@pytest.mark.django_db
def test_buy_total_price(user, cart, item):
    buy = Buy.objects.create(
        user=user,
        cart=cart,
        item_id=item.pk,
        item_quantity=3,
        item_price=item.price,
        phone_number="+380931234567",
        card_number="**** **** **** 1234",
        cvv="***",
        status=True,
    )
    assert buy.get_total_price == 300


@pytest.mark.django_db
def test_last_buy_item_total(user):
    last_buy = LastBuyItem.objects.create(
        user=user, item_name="Chair", price_was=150, quantity=2, item_id=1
    )
    assert last_buy.get_total_price == 300
    assert "Chair x2" in str(last_buy)


@pytest.mark.django_db
def test_comment_creation(user):
    comment = Comment.objects.create(user=user, text="Nice item!")
    assert comment.text == "Nice item!"
    assert comment.user.username == "hamster"
