from django.urls import path, include
from .views import Home, Dashboard, SignUpView, ContactUs, AboutUs, TermsService, Privacy, Conditions, Research
    # FilteredReportsView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('about/', AboutUs.as_view(), name='about_us'),
    path('register/', SignUpView.as_view(), name='register'),
    path('contactus/', ContactUs.as_view(), name='contact_us'),
    path('termsservice/', TermsService.as_view(), name='terms_service'),
    path('privacy/', Privacy.as_view(), name='privacy'),
    path('conditions/', Conditions.as_view(), name='commenting_policy'),
    path('research/', Research.as_view(), name='research'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('reports/', FilteredReportsView.as_view(), name='filtered_reports'),
    ]
