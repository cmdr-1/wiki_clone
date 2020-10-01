from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<entry_page>", views.entry, name="entry_page"),
    path("wiki/search/", views.search, name="search"),
    path("wiki/newpage/", views.newpage, name="newpage"),
    path("wiki/<entry_page>", views.entry, name="reversename"),
    path("wiki/editpage/<entry_page>", views.editpage, name="editpage"),
    path("wiki/randompage/", views.randompage, name="randompage")
]
                                                            