from django.urls import path

from .views import SubmissionDetailView, SubmissionView, SubmissionViewId

urlpatterns = [
    path("", SubmissionView.as_view()),
    path("<str:id>/", SubmissionViewId.as_view()),
    path("view/<str:viewId>/", SubmissionDetailView.as_view()),
]
