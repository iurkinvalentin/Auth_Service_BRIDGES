from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Message, ChatParticipant
from .serializers import ChatSerializer, MessageSerializer, PrivateChatSerializer
from accounts.models import CustomUser


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        """Создание нового чата и добавление создателя как участника"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Сохраняем чат
        chat = serializer.save()

        # Добавляем создателя как участника
        ChatParticipant.objects.create(chat=chat, user=request.user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        """Удаление чата и связанных данных"""
        chat = self.get_object()

        # Удаляем всех участников
        chat.participants.all().delete()

        # Если нужно удалить сообщения (если такая модель существует)
        chat.messages.all().delete()

        # Удаление самого чата
        chat.delete()

        return Response({"detail": "Chat deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class PrivateChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.filter(group=None)  # Личные чаты не связаны с группами
    serializer_class = PrivateChatSerializer

    def create(self, request, *args, **kwargs):
        """Создание нового личного чата"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Получаем участников из запроса
        participants = request.data.get('participants')
    
        # Создаем чат
        chat = Chat.objects.create()

        # Добавляем участников
        for user_id in participants:
            user = CustomUser.objects.get(id=user_id)
            ChatParticipant.objects.create(chat=chat, user=user)

        return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        """Указываем отправителя при создании сообщения"""
        serializer.save(sender=self.request.user)
