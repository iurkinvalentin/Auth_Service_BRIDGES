from rest_framework import viewsets, status
from rest_framework.response import Response
from groups.models import Group, GroupMembership, GroupInvitation
from accounts.models import Profile
from groups.serializers import GroupSerializer, GroupInvitationSerializer
from django.shortcuts import get_object_or_404


class GroupViewSet(viewsets.ViewSet):
    """ViewSet для управления группами и участниками"""

    def list(self, request):
        """Получить список всех групп"""
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Создание новой группы и назначение владельца"""
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            # Создаем группу с указанием владельца (текущий пользователь)
            group = Group.objects.create(
                name=serializer.validated_data['name'],
                description=serializer.validated_data['description'],
                avatar=serializer.validated_data.get('avatar', None),
                owner=request.user  # Указываем текущего пользователя как владельца
            )
            
            # Добавляем владельца группы как участника с ролью 'owner'
            GroupMembership.objects.create(group=group, profile=request.user.profile, role='owner')
            
            return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Получение конкретной группы по id"""
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Обновление существующей группы"""
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """Частичное обновление существующей группы"""
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Удаление группы"""
        group = get_object_or_404(Group, pk=pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def remove_members(self, request, pk=None):
        """Удаление участников из группы"""
        group = get_object_or_404(Group, pk=pk)

        # Проверяем, является ли текущий пользователь владельцем группы
        if not GroupMembership.objects.filter(group=group, profile=request.user.profile, role='owner').exists():
            return Response({'detail': 'У вас нет прав удалять участников'}, status=status.HTTP_403_FORBIDDEN)

        members_data = request.data.get('members', [])
        for member_id in members_data:
            member_profile = get_object_or_404(Profile, pk=member_id)
            
            # Удаляем членство из GroupMembership
            membership = GroupMembership.objects.filter(group=group, profile=member_profile).first()
            if membership:
                membership.delete()
            else:
                return Response({'detail': f'Участник с ID {member_id} не найден в группе'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'detail': 'Участники успешно удалены'}, status=status.HTTP_200_OK)

    def add_members(self, request, pk=None):
        """Добавление участника в группу"""
        group = get_object_or_404(Group, pk=pk)
        member_profile = get_object_or_404(Profile, pk=request.data.get('profile_id'))

        # Проверяем, является ли текущий пользователь владельцем группы
        if not GroupMembership.objects.filter(group=group, profile=request.user.profile, role='owner').exists():
            return Response({'detail': 'У вас нет прав добавлять участников'}, status=status.HTTP_403_FORBIDDEN)

        # Проверяем, не является ли участник уже членом группы
        if GroupMembership.objects.filter(group=group, profile=member_profile).exists():
            return Response({'detail': 'Этот участник уже состоит в группе'}, status=status.HTTP_400_BAD_REQUEST)

        GroupMembership.objects.create(group=group, profile=member_profile, role='member')
        return Response({'detail': 'Участник успешно добавлен'}, status=status.HTTP_200_OK)

    def change_role(self, request, pk=None):
        """Изменение роли участника (может делать только владелец)"""
        group = get_object_or_404(Group, pk=pk)
        member_profile = get_object_or_404(Profile, pk=request.data.get('profile_id'))
        new_role = request.data.get('role')

        # Проверяем, является ли роль валидной
        if new_role not in dict(GroupMembership.ROLE_CHOICES):
            return Response({'detail': 'Недопустимая роль'}, status=status.HTTP_400_BAD_REQUEST)

        # Только владелец может изменять роли
        if not GroupMembership.objects.filter(group=group, profile=request.user.profile, role='owner').exists():
            return Response({'detail': 'У вас нет прав изменять роли'}, status=status.HTTP_403_FORBIDDEN)

        membership = get_object_or_404(GroupMembership, group=group, profile=member_profile)
        membership.role = new_role
        membership.save()

        return Response({'detail': 'Роль успешно изменена'}, status=status.HTTP_200_OK)


class InvitationViewSet(viewsets.ViewSet):
    """ViewSet для управления приглашениями в группу"""

    def create(self, request, pk=None):
        """Отправка приглашения в группу"""
        group = get_object_or_404(Group, pk=pk)
        invited_to_profile = get_object_or_404(Profile, pk=request.data.get('profile_id'))

        # Проверяем, что текущий пользователь является владельцем или администратором группы
        if not GroupMembership.objects.filter(group=group, profile=request.user.profile, role='owner').exists():
            return Response({'detail': 'У вас нет прав приглашать пользователей в эту группу'}, status=status.HTTP_403_FORBIDDEN)

        # Создаем приглашение
        invitation = GroupInvitation.objects.create(
            group=group,
            invited_by=request.user.profile,
            invited_to=invited_to_profile
        )

        return Response(GroupInvitationSerializer(invitation).data, status=status.HTTP_201_CREATED)

    def accept(self, request, pk=None):
        """Принятие приглашения в группу"""
        invitation = get_object_or_404(GroupInvitation, pk=pk, invited_to=request.user.profile)

        if invitation.is_accepted:
            return Response({'detail': 'Это приглашение уже принято'}, status=status.HTTP_400_BAD_REQUEST)

        # Принимаем приглашение
        invitation.is_accepted = True
        invitation.save()

        # Добавляем пользователя в группу
        GroupMembership.objects.create(group=invitation.group, profile=invitation.invited_to, role='member')

        return Response({'detail': 'Приглашение принято, вы добавлены в группу'}, status=status.HTTP_200_OK)

    def decline(self, request, pk=None):
        """Отклонение приглашения в группу"""
        invitation = get_object_or_404(GroupInvitation, pk=pk, invited_to=request.user.profile)

        if invitation.is_accepted:
            return Response({'detail': 'Это приглашение уже принято, его нельзя отклонить'}, status=status.HTTP_400_BAD_REQUEST)

        # Удаляем приглашение
        invitation.delete()
        return Response({'detail': 'Приглашение отклонено'}, status=status.HTTP_204_NO_CONTENT)
