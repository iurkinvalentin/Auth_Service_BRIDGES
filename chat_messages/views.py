from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Message, ChatParticipant
from .serializers import ChatSerializer, MessageSerializer, PrivateChatSerializer
from accounts.models import CustomUser
from rest_framework.decorators import action


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        """Создание нового чата и добавление создателя как участника"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Сохраняем чат
        chat = serializer.save()

        # Добавляем создателя как участника с ролью 'admin'
        ChatParticipant.objects.create(chat=chat, user=request.user, role='admin')

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
    
    @action(detail=False, methods=['get'], url_path='my-chats')
    def list_my_chats(self, request):
        """Получение списка всех чатов, в которых состоит текущий пользователь"""
        user = request.user

        # Фильтруем чаты, в которых участвует текущий пользователь
        chats = Chat.objects.filter(participants__user=user).distinct()

        serializer = self.get_serializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='remove-participant')
    def remove_participant(self, request, pk=None):
        """Удаление участника из группового чата только создателем"""
        chat = self.get_object()

        # Проверка, что текущий пользователь является создателем (админом)
        creator_participant = ChatParticipant.objects.filter(chat=chat, user=request.user, role='admin').first()
        if not creator_participant:
            return Response({"detail": "У вас нет прав удалять участников из этого чата"}, status=status.HTTP_403_FORBIDDEN)

        # Получаем ID пользователя для удаления
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"detail": "Необходимо указать ID пользователя"}, status=status.HTTP_400_BAD_REQUEST)

        # Ищем участника в чате
        participant = ChatParticipant.objects.filter(chat=chat, user__id=user_id).first()
        if not participant:
            return Response({"detail": "Пользователь не найден в этом чате"}, status=status.HTTP_404_NOT_FOUND)

        # Удаляем участника
        participant.delete()

        return Response({"detail": "Участник успешно удалён из чата"}, status=status.HTTP_200_OK)
    

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
