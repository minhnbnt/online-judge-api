from django.urls import path

from .views import ProblemsList, ProblemUpdate

urlpatterns = [
    path("", ProblemsList.as_view()),
    path("<str:id>/", ProblemUpdate.as_view()),
]
