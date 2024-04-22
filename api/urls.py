from django.urls import path
from .views import AuthNumber, AuthCode, InviteCode, Profile, ViewAllInviteUser

urlpatterns = [
    path("auth/", AuthNumber.as_view()),
    path("auth/code/", AuthCode.as_view()),
    path("link/", InviteCode.as_view()),
    path("profile/", Profile.as_view()),
    path("all/user/invited/", ViewAllInviteUser.as_view())
]
