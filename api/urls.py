from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import ProblemsList, ProblemUpdate, UserRegister, hello

urlpatterns = [
    path("hello/", hello),
    #
    path("problems/", ProblemsList.as_view()),
    path("problems/<str:id>/", ProblemUpdate.as_view()),
    #
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
    #
    path("register/", UserRegister.as_view()),
]
