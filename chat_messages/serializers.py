from rest_framework import serializers
from .models import Chat, Message, ChatParticipant
from accounts.models import CustomUser

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),  # или Profile.objects.all() в зависимости от модели
        many=True,
        required=False  # Поле не обязательно
    )

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



class ChatParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatParticipant
        fields = '__all__'
