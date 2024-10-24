from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ChatViewSet, MessageViewSet, PrivateChatViewSet

router = DefaultRouter()
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'private-chats', PrivateChatViewSet, basename='private-chat') 

urlpatterns = [
    path('', include(router.urls)),
]