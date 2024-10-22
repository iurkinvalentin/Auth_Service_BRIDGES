from rest_framework.routers import DefaultRouter
from groups.views import GroupViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')

urlpatterns = [
    path('groups/<int:pk>/add_members/', GroupViewSet.as_view({'post': 'add_members'}), name='group-add-members'),
    path('groups/<int:pk>/remove_members/', GroupViewSet.as_view({'post': 'remove_members'}), name='group-remove-members'),
] + router.urls