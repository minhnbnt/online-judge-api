from django.urls import path

from .views import getProblemDetail, getProblems, hello

urlpatterns = [
    path("hello/", hello),
    path("problems/", getProblems),
    path("problems/detail/<str:idDisplay>", getProblemDetail),
]
