from django.urls import path

from .views import ProblemsListView, ProblemDetailView

urlpatterns = [
    path("", ProblemsListView.as_view()),
    path("<str:id>/", ProblemDetailView.as_view()),
]
