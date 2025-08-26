from django import forms
from django.db.models import Max, Min

from account.models import Comment
from service.models import Item, ItemClass


class SearchItemForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search", "class": "form-control"}
        ),
    )


class PriceFilterForm(forms.Form):
    min_price = forms.DecimalField(required=False, label="Min price", decimal_places=2)
    max_price = forms.DecimalField(required=False, label="Max price", decimal_places=2)

    def __init__(self, *args, **kwargs):
        min_value = kwargs.pop("min_value", None)
        max_value = kwargs.pop("max_value", None)
        super().__init__(*args, **kwargs)

        if min_value is not None:
            self.fields["min_price"].label = f"Min price ({round(min_value, 2)})"
        if max_value is not None:
            self.fields["max_price"].label = f"Max price ({round(max_value, 2)})"


class FilterClassForm(forms.Form):
    class_name = forms.ModelChoiceField(
        queryset=ItemClass.objects.all(),
        required=False,
        label="Class",
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": ""}
