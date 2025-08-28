from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Min, Max
from django.db.transaction import commit
from django.urls.base import reverse, reverse_lazy
from django.views import generic
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import FormMixin

from account.models import Comment
from service.forms import SearchItemForm, PriceFilterForm, FilterClassForm, CommentForm
from service.models import Item, ItemClass


def index(request: HttpRequest) -> HttpResponse:
    num_item = Item.objects.all().count()
    num_class = ItemClass.objects.all().count()
    context = {"num_item": num_item, "num_class": num_class}
    return render(request, "service/index.html", context=context)


class ItemListView(generic.ListView):
    model = Item
    template_name = "service/item_list.html"
    paginate_by = 9

    def get_queryset(self):
        queryset = Item.objects.select_related("color", "item_class").prefetch_related(
            "material", "comment"
        )
        self.search_form = SearchItemForm(self.request.GET)
        self.filter_form = PriceFilterForm(self.request.GET)
        self.class_filter = FilterClassForm(self.request.GET)
        self.sort_by = self.request.GET.get("sort_price")
        if self.sort_by == "price_asc":
            queryset = queryset.order_by("price")
        elif self.sort_by == "price_desc":
            queryset = queryset.order_by("-price")

        if self.class_filter.is_valid():
            selected_class = self.class_filter.cleaned_data.get("class_name")
            if selected_class:
                queryset = queryset.filter(item_class__name=selected_class)
        if self.search_form.is_valid():
            name = self.search_form.cleaned_data.get("name")
            if name:
                queryset = queryset.filter(
                    name__icontains=name,
                )
        if self.filter_form.is_valid():
            min_price = self.filter_form.cleaned_data.get("min_price")
            max_price = self.filter_form.cleaned_data.get("max_price")
            if min_price is not None:
                queryset = queryset.filter(price__gte=min_price)
            if max_price is not None:
                queryset = queryset.filter(price__lte=max_price)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        filtered_queryset = self.get_queryset()
        price_bounds = filtered_queryset.aggregate(
            min_price=Min("price"), max_price=Max("price")
        )

        context["search_form"] = self.search_form
        context["sort_price"] = self.sort_by
        context["filter_form"] = PriceFilterForm(
            self.request.GET,
            min_value=price_bounds["min_price"],
            max_value=price_bounds["max_price"],
        )
        context["class_filter"] = self.class_filter
        return context


class ItemDetailView(FormMixin, generic.DetailView):
    model = Item
    template_name = "service/item_detail.html"
    queryset = Item.objects.prefetch_related("comment__user", "comment")

    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy("service:item-detail", kwargs={"pk": self.kwargs["pk"]})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.save()
        self.object.comment.add(comment)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["comment_form"] = self.get_form()
        return context


class ItemCreateView(UserPassesTestMixin, generic.CreateView):
    model = Item
    fields = (
        "name",
        "price",
        "description",
        "color",
        "material",
        "count",
        "item_class",
        "image",
    )
    template_name = "service/item_form.html"
    success_url = reverse_lazy("service:item-list")

    def test_func(self):
        return self.request.user.is_superuser



class ItemUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Item
    fields = (
        "name",
        "price",
        "description",
        "color",
        "material",
        "count",
        "item_class",
        "image",
    )
    template_name = "service/item_form.html"
    success_url = reverse_lazy("service:item-list")

    def test_func(self):
        return self.request.user.is_superuser


class ItemDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Item
    success_url = reverse_lazy("service:item-list")

    def test_func(self):
        return self.request.user.is_superuser


class CommentDelete(generic.DeleteView):
    model = Comment

    def get_success_url(self):
        item = self.object.items.first()
        return reverse_lazy("service:item-detail", kwargs={"pk": item.pk})

