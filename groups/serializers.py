from rest_framework import serializers
from groups.models import Group, GroupMembership, GroupInvitation


class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    members = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'avatar', 'created_at', 'updated_at', 'owner', 'members']

    def get_members(self, obj):
        """Извлекаем участников группы через модель GroupMembership"""
        memberships = GroupMembership.objects.filter(group=obj)
        return [{'profile_id': membership.profile.id, 'role': membership.role} for membership in memberships]

    def create(self, validated_data):
        """Создание новой группы"""
        # Создаем группу с переданными данными
        group = Group.objects.create(**validated_data)
        
        # Добавляем владельца в качестве участника группы с ролью 'owner'
        GroupMembership.objects.create(group=group, profile=self.context['request'].user.profile, role='owner')
        
        return group

    def update(self, instance, validated_data):
        """Обновление группы"""
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()

        return instance


class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = ['group', 'profile', 'role', 'date_joined']

    def update(self, instance, validated_data):
        """Переопределение метода для обновления роли участника"""
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance
    

class GroupInvitationSerializer(serializers.ModelSerializer):
    invited_by = serializers.ReadOnlyField(source='invited_by.user.username')
    invited_to = serializers.ReadOnlyField(source='invited_to.user.username')
    group = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = GroupInvitation
        fields = ['id', 'group', 'invited_by', 'invited_to', 'created_at', 'is_accepted']