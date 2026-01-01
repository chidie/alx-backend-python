from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Conversation, Message, Notification

User = get_user_model()

class MessageNotificationTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            email="sender@example.com",
            password="password123",
            first_name="Sender",
            last_name="User",
            role="guest",
        )

        self.receiver = User.objects.create_user(
            email="receiver@example.com",
            password="password123",
            first_name="Receiver",
            last_name="User",
            role="host",
        )
        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.sender, self.receiver])
    
    def test_notification_created_on_new_message(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            conversation=self.conversation,
            message_body="Hello, this is a test message."
        )
        notification = Notification.objects.filter(user=self.receiver, message=message)
        self.assertEqual(notification.count(), 1)
    
    def test_no_notification_on_message_update(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            conversation=self.conversation,
            message_body="Initial message."
        )
        # Clear existing notifications
        Notification.objects.all().delete()

        # Update the message
        message.message_body = "Updated message."
        message.save()

        notification = Notification.objects.filter(user=self.receiver, message=message)
        self.assertEqual(notification.count(), 0)
# Create your tests here.
