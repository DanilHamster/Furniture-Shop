import pytest
from service.forms import SearchItemForm, PriceFilterForm, FilterClassForm, CommentForm
from service.models import ItemClass
from account.models import Comment
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def item_class(db):
    return ItemClass.objects.create(name="Furniture")


@pytest.fixture
def user(db):
    return User.objects.create_user(username="user", password="pass")


def test_search_item_form_valid():
    form = SearchItemForm(data={"name": "Table"})
    assert form.is_valid()
    assert form.cleaned_data["name"] == "Table"


def test_search_item_form_empty():
    form = SearchItemForm(data={})
    assert form.is_valid()
    assert form.cleaned_data["name"] == ""


def test_price_filter_form_labels():
    form = PriceFilterForm(min_value=10, max_value=100)
    assert "Min price (10)" in form.fields["min_price"].label
    assert "Max price (100)" in form.fields["max_price"].label


def test_price_filter_form_valid_range():
    form = PriceFilterForm(data={"min_price": 20, "max_price": 80})
    assert form.is_valid()
    assert form.cleaned_data["min_price"] == 20
    assert form.cleaned_data["max_price"] == 80


def test_price_filter_form_invalid_decimal():
    form = PriceFilterForm(data={"min_price": "abc"})
    assert not form.is_valid()
    assert "min_price" in form.errors


@pytest.mark.django_db
def test_filter_class_form_valid(item_class):
    form = FilterClassForm(data={"class_name": item_class.pk})
    assert form.is_valid()
    assert form.cleaned_data["class_name"] == item_class


@pytest.mark.django_db
def test_comment_form_valid(user):
    form = CommentForm(data={"text": "Great item!"})
    assert form.is_valid()
    comment = form.save(commit=False)
    comment.user = user
    comment.save()
    assert Comment.objects.count() == 1
    assert Comment.objects.first().text == "Great item!"
