import pytest
from service.models import Color, Material, Item, ItemClass
from account.models import Comment


@pytest.fixture
def color(db):
    return Color.objects.create(color="Red")


@pytest.fixture
def material(db):
    return Material.objects.create(material="Wood")


@pytest.fixture
def item_class(db):
    return ItemClass.objects.create(name="Furniture")


@pytest.fixture
def comment(db, django_user_model):
    user = django_user_model.objects.create_user(username="hamster", password="pass")
    return Comment.objects.create(user=user, text="Nice item!")


def test_color_str(color):
    assert str(color) == "Red"


def test_material_str(material):
    assert str(material) == "Wood"


def test_item_class_str(item_class):
    assert str(item_class) == "Furniture"


@pytest.mark.django_db
def test_item_creation(color, material, item_class, comment):
    item = Item.objects.create(
        name="Chair",
        price=199.99,
        count=5,
        color=color,
        item_class=item_class,
        description="Comfortable chair",
    )
    item.material.add(material)
    item.comment.add(comment)

    assert item.name == "Chair"
    assert item.price == 199.99
    assert item.count == 5
    assert item.color.color == "Red"
    assert item.item_class.name == "Furniture"
    assert item.material.first().material == "Wood"
    assert item.comment.first().text == "Nice item!"
    assert str(item) == "Item: Chair, Price: 199.99"


@pytest.mark.django_db
def test_item_get_image_url_without_image(color, item_class):
    item = Item.objects.create(
        name="Chair", price=100, count=1, color=color, item_class=item_class
    )
    assert item.get_image_url() == "/static/img/placeholder.png"
