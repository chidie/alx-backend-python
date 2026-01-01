from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if not created:
        return # Only create notification for newly created messages
    Notification.objects.create(
        user=instance.receiver,
        message=instance
    )

@receiver(post_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return # New message, no need to log on creation
    
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return # Old instance doesn't exist, nothing to log

    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content
        )
        instance.edited = True