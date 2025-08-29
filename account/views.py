from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from account.forms import CartItemForm, UserProfileUpdateForm, BuyForm
from account.models import User, Cart, CartItem, Buy, LastBuyItem
from service.models import Item
import logging
from base64 import urlsafe_b64encode

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode
from django.views import generic, View

from account.forms import CustomUserCreationForm
from account.services.token_service import account_activation_token


logger = logging.getLogger(__name__)

User = get_user_model()


class CartAccountDetailView(generic.DetailView):
    model = Cart
    template_name = "accounts/cart.html"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartItemUpdateView(generic.UpdateView):
    form_class = CartItemForm
    model = CartItem
    template_name = "accounts/cart_item_form.html"

    def get_success_url(self):
        return reverse_lazy("accounts:cart-acc", kwargs={"pk": self.object.cart.id})


class BuyFormView(generic.FormView):
    form_class = BuyForm
    model = Buy
    template_name = "accounts/buy_form.html"

    def form_valid(self, form):
        phone = form.cleaned_data.get("phone_number")
        card = form.cleaned_data.get("card_number")
        mask_card = f"**** **** **** {card[-4:]}"
        user = self.request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_items = cart.items.all()

        for item in cart_items:
            LastBuyItem.objects.create(
                user=user,
                item_name=item.item.name,
                price_was=item.item.price,
                quantity=item.quantity,
                item_id=item.item.pk,
            )

            item.item.count = max(item.item.count - item.quantity, 0)
            item.item.save()

            Buy.objects.create(
                cvv="***",
                card_number=mask_card,
                phone_number=phone,
                user=user,
                cart=cart,
                item_id=item.item.pk,
                item_price=item.item.price,
                item_quantity=item.quantity,
                status=True,
            )

            item.delete()

        return redirect("index")


class LastBuyDeleteView(generic.DeleteView):
    model = LastBuyItem

    def get_success_url(self):
        return reverse_lazy("accounts:account-profile")


class AddToCartView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        item_id = request.POST.get("item_id")
        item = get_object_or_404(Item, pk=item_id)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item = CartItem.objects.filter(cart=cart, item=item).first()

        if cart_item and item.count > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            CartItem.objects.get_or_create(
                cart=cart, item=item, defaults={"quantity": 1}
            )

        return redirect("accounts:cart-acc", cart.id)

    def get(self, request: HttpRequest) -> HttpResponse:
        return redirect("accounts:cart-acc", request.user.cart.id)


class CartItemDeleteView(generic.DeleteView):
    model = CartItem

    def get_success_url(self):
        return reverse_lazy("accounts:cart-acc", kwargs={"pk": self.object.cart.id})


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/sign_up.html"
    model = User

    def form_valid(self, form: CustomUserCreationForm):
        try:
            with transaction.atomic():
                form.instance.is_active = False
                user = form.save()

                mail_subject = "Email confirmation"

                scheme = self.request.scheme
                domain = get_current_site(self.request).domain
                uid = urlsafe_b64encode(force_bytes(user.pk)).decode()
                token = account_activation_token.make_token(user)

                url = f"{scheme}://{domain}/accounts/activate/{uid}/{token}/"

                html_content = render_to_string(
                    "registration/emails/acc_active_email.html",
                    {"url": url, "user": user},
                )

                email = EmailMessage(mail_subject, html_content, to=[user.email])
                email.content_subtype = "html"

                email.send()
        except Exception as e:
            logger.error(f"Error sending email: {e}")

            return super().form_invalid(form)

        return render(self.request, "registration/email_confirmation_sent.html")


class ActivateAccountView(View):
    def get(self, request: HttpRequest, uid: str, token: str):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None:
            if user.is_active:
                messages.info(request, "Your account is already activated.")

                return redirect("accounts:login")

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()

                messages.success(
                    request,
                    "Thank you for confirming your email. You can now login to your account.",
                )
                return redirect("accounts:login")

        return render(request, "registration/activation_invalid.html")


class ProfileView(generic.DetailView):
    model = User
    template_name = "accounts/userprofile.html"

    def get_object(self):
        return self.request.user


class ProfileUpdateView(generic.UpdateView):
    model = User
    form_class = UserProfileUpdateForm
    template_name = "accounts/userprofileupdate.html"
    success_url = reverse_lazy("accounts:account-profile")

    def get_object(self, queryset=None):
        return self.request.user


class BuyListView(generic.ListView):
    model = Buy
    template_name = "accounts/buy_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        buy_list = context["buy_list"]

        item_map = {
            item.id: item.name
            for item in Item.objects.filter(id__in=[item.item_id for item in buy_list])
        }

        for item in buy_list:
            item.item_name = item_map.get(item.item_id, "Unknown item")

        return context


class BuyInfoDeleteView(generic.DeleteView):
    model = Buy
    success_url = reverse_lazy("accounts:buy-list")
