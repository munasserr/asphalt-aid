from django.urls import path
from users_app.api.views.auth import SignupView, SigninView
from users_app.api.views.user import UserProfileView, UserUpdateView, ChangePasswordView

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/signin/", SigninView.as_view(), name="signin"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("profile/update/", UserUpdateView.as_view(), name="user-update"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
