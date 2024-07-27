from django.urls import include, path

from .views import hello, runtimes

urlpatterns = [
    path("hello/", hello),
    path("runtimes/", runtimes),
    path("token/", include("api.token.urls")),
    path("users/", include("api.users.urls")),
    path("schemas/", include("api.schemas.urls")),
    path("problems/", include("api.problems.urls")),
    path("submissions/", include("api.submissions.urls")),
]
