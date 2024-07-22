from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import TokenObtainPairView

urlpatterns = [
    path("", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
