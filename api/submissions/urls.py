from django.urls import path

from .views import SubmissionDetailView, SubmissionView, SubmissionViewId

urlpatterns = [
    path("", SubmissionView.as_view()),
    path("get/<str:id>", SubmissionViewId.as_view()),
    path("<str:viewId>", SubmissionDetailView.as_view()),
]
