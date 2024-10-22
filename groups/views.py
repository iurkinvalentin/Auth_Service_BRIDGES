from rest_framework import viewsets, status
from rest_framework.response import Response
from groups.models import Group
from accounts.models import Profile
from groups.serializers import GroupSerializer
from django.shortcuts import get_object_or_404


class GroupViewSet(viewsets.ViewSet):
    """ViewSet для управления группами"""

    def list(self, request):
        """Получить список всех групп"""
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Создание новой группы"""
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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

    def add_members(self, request, pk=None):
        """Добавление участников в группу"""
        group = get_object_or_404(Group, pk=pk)
        members_data = request.data.get('members', [])
        for member_id in members_data:
            member = get_object_or_404(Profile, pk=member_id)
            group.members.add(member)
        group.save()
        return Response({'detail': 'Участники успешно добавлены'}, status=status.HTTP_200_OK)

    def remove_members(self, request, pk=None):
        """Удаление участников из группы"""
        group = get_object_or_404(Group, pk=pk)
        members_data = request.data.get('members', [])
        for member_id in members_data:
            member = get_object_or_404(Profile, pk=member_id)
            group.members.remove(member)
        group.save()
        return Response({'detail': 'Участники успешно удалены'}, status=status.HTTP_200_OK)
