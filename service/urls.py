from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from service.views import ItemListView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView, CommentDelete

app_name = "service"

urlpatterns = [
    path("item/", ItemListView.as_view(), name="item-list"),
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("item/create/", ItemCreateView.as_view(), name="item-create"),
    path("item/<int:pk>/update/", ItemUpdateView.as_view(), name="item-update"),
    path("item-del/<int:pk>/", ItemDeleteView.as_view(), name="item-del"),
    path("comment/<int:pk>/", CommentDelete.as_view(), name="comment-del"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

