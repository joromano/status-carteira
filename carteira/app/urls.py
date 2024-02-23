from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_page, name="login_page"),
    path("accounts/logout/", views.logout_page, name="logout_page"),
    path("history/", views.history, name="history"),
    path("add/", views.add_entry, name="add_entry"),
    path("remove/<int:id>/", views.remove_entry, name="remove_entry"),
    path("delete/<int:id>/", views.delete_entry, name="delete_entry"),

]