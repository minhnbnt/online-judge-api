from django.urls import path

from .views import UserRegisterView, UserInfoView

urlpatterns = [
    path("info/<int:id>/", UserInfoView.as_view()),
    path("register/", UserRegisterView.as_view()),
]
