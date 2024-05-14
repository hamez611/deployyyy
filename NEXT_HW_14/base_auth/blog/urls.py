from .views import home, new, detail, edit, delete, delete_comment, my_page, subscribe
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home"),
    path("new/", new, name="new"),
    path("detail/<int:post_pk>", detail, name="detail"),
    path("edit/<int:post_pk>", edit, name="edit"),
    path("delete/<int:post_pk>", delete, name="delete"),
    path(
        "delete-comment/<int:comment_pk>",
        delete_comment,
        name="delete_comment",
    ),
    path("mypage/<int:owner_pk>", my_page, name="my-page"),
    path("subscribe/<int:owner_pk>", subscribe, name="subscribe"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
