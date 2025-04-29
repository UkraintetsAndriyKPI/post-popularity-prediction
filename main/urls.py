from django.urls import path

from .views import (
    index, faq,
    profile, update_profile,
    login_page, logout_page, register_page)

urlpatterns = [
    path("", index, name="index"),
    path("faq/", faq, name="faq"),
    path("profile/", profile, name="profile"),
    path("profile/update", update_profile, name="update_profile"),

    path("login/", login_page, name="login_page"),
    path("logout/", logout_page, name="logout_page"),
    path("register/", register_page, name="register_page"),
]
