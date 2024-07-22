from django.urls import include, path

from .views import UserRegister, hello, runtimes

urlpatterns = [
    path("hello/", hello),
    path("runtimes/", runtimes),
    path("register/", UserRegister.as_view()),
    path("token/", include("api.token.urls")),
    path("problems/", include("api.problems.urls")),
    path("submissions/", include("api.submissions.urls")),
    path("schema/", include("api.schema.urls")),
]
