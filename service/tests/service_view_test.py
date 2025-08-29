import pytest
from django.urls import reverse
from service.models import Item, ItemClass, Color
from account.models import Comment
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def item_class(db):
    return ItemClass.objects.create(name="TestClass")


@pytest.fixture
def color(db):
    return Color.objects.create(color="Red")


@pytest.fixture
def user(db):
    return User.objects.create_user(username="user", password="pass")


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(
        username="admin", password="pass", email="admin@example.com"
    )


@pytest.fixture
def item(db, item_class, color):
    return Item.objects.create(
        name="Test Item", price=10, count=1, color=color, item_class=item_class
    )


@pytest.mark.django_db
def test_index_view_context(client, item_class, color):
    Item.objects.create(
        name="Test Item", price=10, count=1, color=color, item_class=item_class
    )
    response = client.get(reverse("index"))
    assert response.status_code == 200
    assert response.context["num_item"] == 1
    assert response.context["num_class"] == 1


@pytest.mark.django_db
def test_item_detail_comment_post(client, user, item):
    client.force_login(user)
    comment_text = "This is a test comment."
    response = client.post(
        reverse("service:item-detail", kwargs={"pk": item.pk}),
        {"text": comment_text},
        follow=True,
    )
    assert response.status_code == 200
    comment = Comment.objects.first()
    assert comment.text == comment_text
    assert comment.user == user


@pytest.mark.django_db
def test_item_create_view_requires_superuser(client, user):
    client.force_login(user)
    response = client.get(reverse("service:item-create"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_item_delete_view_allowed_for_superuser(client, superuser, item):
    client.force_login(superuser)
    assert Item.objects.count() == 1
    response = client.post(
        reverse("service:item-del", kwargs={"pk": item.pk}), follow=True
    )
    assert response.status_code == 200
    assert Item.objects.count() == 0
