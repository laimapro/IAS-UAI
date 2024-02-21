from django.urls import path
from .views import (CreateInstanceView, SurveyStartView, SurveyQuestionView, SurveyFinishedView)

urlpatterns = [
    # path('', ListProjects.as_view(), name='instance_list'),
    path('import/<uuid:project_id>/', CreateInstanceView.as_view(), name='instance_import'),
    path('survey/<uuid:instance_id>/', SurveyStartView.as_view(), name='survey_start'),
    path('survey_finished/', SurveyFinishedView.as_view(), name='survey_finished'),
    path('survey_question/<uuid:attempt_id>/<int:q>/', SurveyQuestionView.as_view(), name='survey_question'),
    ]
