from django.urls import path
from .views import QuestionBatchView

urlpatterns = [
    path('batch/', QuestionBatchView.as_view(), name="question_batch"),
    ]