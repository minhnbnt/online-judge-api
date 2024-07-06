from django.urls import path

from .views import ProblemsList, ProblemUpdate, hello

urlpatterns = [
    path("hello/", hello),
    path("problems/", ProblemsList.as_view()),
    path("problems/<str:id>/", ProblemUpdate.as_view()),
]
