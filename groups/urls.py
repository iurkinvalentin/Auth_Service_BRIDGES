from rest_framework.routers import DefaultRouter
from groups.views import GroupViewSet, InvitationViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'invitations', InvitationViewSet, basename='invitation')

urlpatterns = [
    path('groups/<int:pk>/add_members/', GroupViewSet.as_view({'post': 'add_members'}), name='group-add-members'),
    path('groups/<int:pk>/remove_members/', GroupViewSet.as_view({'post': 'remove_members'}), name='group-remove-members'),
    path('groups/<int:pk>/change_role/', GroupViewSet.as_view({'post': 'change_role'}), name='group-change-role')
] + router.urls