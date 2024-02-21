from django.urls import path
from .views import (ListProjects, DetailProject, CreateProjectView, EditProject, DeleteProject, InvitationView,
                    ParticipantInvitationView)

urlpatterns = [
    path('', ListProjects.as_view(), name='pj_list'),
    path('new/', CreateProjectView.as_view(), name='pj_new'),
    path('detail/<uuid:id>/', DetailProject.as_view(), name='pj_detail'),
    path('edit/<uuid:id>/', EditProject.as_view(), name='pj_edit'),
    path('delete/<uuid:id>/', DeleteProject.as_view(), name='pj_delete'),
    path('invitation/<int:type>/<uuid:id>/', InvitationView.as_view(), name='pj_invitation'),
    path('invite/<uuid:id>/', ParticipantInvitationView.as_view(), name='pj_invite'),
    ]
