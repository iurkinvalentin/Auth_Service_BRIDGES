from rest_framework import serializers
from .models import Chat, Message, ChatParticipant
from accounts.models import CustomUser

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = '__all__'

class ChatParticipantSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')  # Отображаем имя пользователя

    class Meta:
        model = ChatParticipant
        fields = ['user', 'role']  # Включаем роль участника

class ChatSerializer(serializers.ModelSerializer):
    participants = ChatParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'participants', 'created_at']

    def create(self, validated_data):
        # Извлекаем список участников из данных
        participants_data = validated_data.pop('participants', [])
        
        # Создаем сам чат
        chat = Chat.objects.create(**validated_data)

        # Добавляем участников в ChatParticipant
        for user in participants_data:
            ChatParticipant.objects.create(chat=chat, user=user)

        return chat

    def update(self, instance, validated_data):
        # Извлекаем список участников
        participants_data = validated_data.pop('participants', None)

        # Обновляем сам чат
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        # Если список участников был передан, обновляем участников
        if participants_data is not None:
            instance.participants.clear()  # Очистим текущих участников
            for user in participants_data:
                ChatParticipant.objects.create(chat=instance, user=user)

        return instance
    

class PrivateChatSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        many=True
    )

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'created_at']

    def create(self, validated_data):
        participants = validated_data['participants']
        if len(participants) != 2:
            raise serializers.ValidationError("Личные чаты могут включать только двух участников.")
        
        # Фильтрация через связь участников
        existing_chat = Chat.objects.filter(
            participants__user__in=participants  # Правильная связь через related_name 'participants'
        ).distinct().first()

        if existing_chat:
            return existing_chat

        # Создание нового чата
        chat = Chat.objects.create()
        for participant in participants:
            ChatParticipant.objects.create(chat=chat, user=participant)
        
        return chat

