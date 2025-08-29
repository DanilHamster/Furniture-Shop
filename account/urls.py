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
    LastBuyDeleteView,
    BuyListView,
    BuyInfoDeleteView,
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
    path("cart/<int:pk>/item/update/", CartItemUpdateView.as_view(), name="cart-item"),
    path("buy/", BuyFormView.as_view(), name="buy-form"),
    path("add-to-cart/", AddToCartView.as_view(), name="add-to-cart"),
    path("item/<int:pk>/delete", CartItemDeleteView.as_view(), name="del-item"),
    path("profile/", ProfileView.as_view(), name="account-profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="account-profile-update"),
    path(
        "last_buy/<int:pk>/delete/", LastBuyDeleteView.as_view(), name="last-buy-delete"
    ),
    path("admin/buy_list/", BuyListView.as_view(), name="buy-list"),
    path("admin/<int:pk>/del_buy/", BuyInfoDeleteView.as_view(), name="buy-del"),
]
