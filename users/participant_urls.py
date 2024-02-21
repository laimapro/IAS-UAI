from django.urls import path
from users.views import ListParticipants, DetailParticipant, ParticipantSignUp, ParticipantEditView
from .import views

urlpatterns = [
    path('', ListParticipants.as_view(), name='participant_list'),
    # path('detail/<uuid:id>/', DetailParticipant.as_view(), name='participant_detail'),
    path('signup/<str:project_id>', ParticipantSignUp.as_view(), name="participant_signup"),
    path('profile/', ParticipantEditView.as_view(), name="participant_edit"),
    ]
