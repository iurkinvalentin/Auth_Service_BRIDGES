from django.db import models
from accounts.models import CustomUser
from groups.models import Group


class Chat(models.Model):
    """Модель для чатов. Может быть индивидуальный или групповой чат."""
    name = models.CharField(max_length=255, blank=True, null=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, blank=True, related_name='chat')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else f"Chat {self.id}"


class Message(models.Model):
    """Модель для сообщений."""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message from {self.sender.username} in Chat {self.chat.id}"


class ChatParticipant(models.Model):
    """Модель участников чата."""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in Chat {self.chat.id}"
