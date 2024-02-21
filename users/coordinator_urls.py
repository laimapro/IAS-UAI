from django.urls import path
from users.views import CoordinatorSignUp, CoordinatorEditView

urlpatterns = [
    # path('', ListCompanies.as_view(), name='company_list'),
    # path('detail/<int:pk>/', DetailCompany.as_view(), name='company_detail'),
    path('signup/<str:project_id>/', CoordinatorSignUp.as_view(), name="coordinator_signup"),
    path('profile/', CoordinatorEditView.as_view(), name="coordinator_edit"),
    ]
