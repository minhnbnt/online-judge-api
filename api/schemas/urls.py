from django.urls import path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("", SpectacularAPIView.as_view()),
    path("swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema")),
]
