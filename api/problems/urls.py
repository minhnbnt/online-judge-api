from django.urls import path

from .views import ProblemsListView, ProblemDetailView, CommentListView

urlpatterns = [
    path("", ProblemsListView.as_view()),
    path("<str:id>/", ProblemDetailView.as_view()),
    path("<str:id>/comments/", CommentListView.as_view()),
]
