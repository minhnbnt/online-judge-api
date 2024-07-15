from django.urls import include, path

from .views import UserRegister, hello

urlpatterns = [
    path("hello/", hello),
    path("register/", UserRegister.as_view()),
    path("token/", include("api.token.urls")),
    path("problems/", include("api.problems.urls")),
    path("submissions/", include("api.submissions.urls")),
]
