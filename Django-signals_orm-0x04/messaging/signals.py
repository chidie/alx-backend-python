from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

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

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications related to the deleted user
    Notification.objects.filter(user=instance).delete()

    # Delete messages sent or received by the user (message history)
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()