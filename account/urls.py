from django.urls import path, include

from account.views import (
    CartAccountDetailView,
    CartItemUpdateView,
    BuyFormView,
    AddToCartView,
    CartItemDeleteView,
    SignUpView,
    ActivateAccountView,
    ProfileView,
    ProfileUpdateView,
    OrderDeleteView,
    OrderListView,
    OrderInfoDeleteView,
)

app_name = "accounts"

urlpatterns = [
    path("signup", SignUpView.as_view(), name="sign-up"),
    path(
        "activate/<str:uid>/<str:token>/",
        ActivateAccountView.as_view(),
        name="activate",
    ),
    path("", include("django.contrib.auth.urls")),
    path("cart/<int:pk>/", CartAccountDetailView.as_view(), name="cart-acc"),
    path(
        "cart/<int:pk>/item/update/",
        CartItemUpdateView.as_view(),
        name="cart-item",
    ),
    path("buy_form/", BuyFormView.as_view(), name="buy-form"),
    path("add_to_cart/", AddToCartView.as_view(), name="add-to-cart"),
    path(
        "item/<int:pk>/delete", CartItemDeleteView.as_view(), name="del-item"
    ),
    path("profile/", ProfileView.as_view(), name="account-profile"),
    path(
        "profile/update/",
        ProfileUpdateView.as_view(),
        name="account-profile-update",
    ),
    path(
        "order/<int:pk>/delete/",
        OrderDeleteView.as_view(),
        name="order-delete",
    ),
    path("admin/order_list/", OrderListView.as_view(), name="order-list"),
    path(
        "admin/<int:pk>/del_buy/",
        OrderInfoDeleteView.as_view(),
        name="buy-del",
    ),
]
