from django.contrib import admin
from django.urls import path
from accounts.views import UserListView, ProfileDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserListView.as_view(), name='user-list'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
]
