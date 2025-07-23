from django.urls import path
from .views import UserProfileView, RegisterView, StaffUserListView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('staff/', StaffUserListView.as_view(), name='staff-list'),
]