from rest_framework import serializers
from groups.models import Group
from accounts.models import Profile


class GroupSerializer(serializers.ModelSerializer):
    # Используем поле для передачи и получения списка ID участников
    members = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), many=True)

    class Meta:
        model = Group
        fields = '__all__'

    def create(self, validated_data):
        """Переопределяем метод создания группы с участниками"""
        members_data = validated_data.pop('members', None)  # Извлекаем данные участников
        group = Group.objects.create(**validated_data)
        if members_data:
            group.members.set(members_data)  # Устанавливаем участников группы
        return group

    def update(self, instance, validated_data):
        """Переопределяем метод обновления группы"""
        members_data = validated_data.pop('members', None)  # Извлекаем данные участников
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()

        if members_data:
            instance.members.set(members_data)  # Обновляем участников группы
        return instance