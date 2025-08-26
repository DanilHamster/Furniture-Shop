from django.urls import path, include

from account.views import (
    CartAccountDetailView,
    CartItemUpdateView,
    BuyForm,
    add_to_cart,
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
    path("cart/item/<int:pk>/", CartItemUpdateView.as_view(), name="cart-item"),
    path("buy/", BuyForm.as_view(), name="buy-form"),
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    path("del-item/<int:pk>/", CartItemDeleteView.as_view(), name="del-item"),
    path("profile/", ProfileView.as_view(), name="account-profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="account-profile-update"),
    path(
        "last_buy/delete/<int:pk>/", LastBuyDeleteView.as_view(), name="last-buy-delete"
    ),
    path("admin/buy_list/", BuyListView.as_view(), name="buy-list"),
    path("admin/del_buy/<int:pk>/", BuyInfoDeleteView.as_view(), name="buy-del"),
]
