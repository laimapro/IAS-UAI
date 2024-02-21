from django.urls import path
from users.views import ListCompanies, DetailCompany, CompanySignUp, CompanyEditView

urlpatterns = [
    path('', ListCompanies.as_view(), name='company_list'),
    path('detail/<int:pk>/', DetailCompany.as_view(), name='company_detail'),
    path('signup/<str:project_id>/', CompanySignUp.as_view(), name="company_signup"),
    path('profile/', CompanyEditView.as_view(), name="company_edit"),
    ]
