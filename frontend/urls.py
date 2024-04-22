from django.urls import path
from .views import auth, check_code, user, link_user

urlpatterns = [
    path("", auth),
    path("auth/code/", check_code),
    path("user/", user),
    path("link_user/", link_user)

]