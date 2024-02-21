from django.urls import path
from users.views import UserActivateView

urlpatterns = [
    path('activate/<str:user_id>/<str:token>/', UserActivateView.as_view(), name="user_activate"),
    ]
