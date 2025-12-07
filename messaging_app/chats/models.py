import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password_hash = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.role})"
    
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, related_name="message_sent", on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender_id.email}"
    
# class Property(models.Model):
#     property_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     host = models.ForeignKey(User, related_name="properties", on_delete=models.CASCADE)
#     title = models.CharField(max_length=255, null=False, blank=False)
#     description = models.TimeField(null=False, blank=False)
#     location = models.CharField(max_length=255, null=False, blank=False)
#     price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} located at {self.location}"

# class Booking(models.Model):
#     booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     property = models.ForeignKey(Property, related_name="bookings", on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name="bookings", on_delete=models.CASCADE)

#     STATUS_CHOICES = [
#         ("pending", "Pending"),
#         ("confirmed", "Confirmed"),
#         ("cancelled", "Canceled"),
#     ]
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

#     check_in = models.DateField(null=False, blank=False)
#     check_out = models.DateField(null=False, blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Booking {self.booking_id} for {self.property.title}"

# class Payment(models.Model):
#     payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     booking = models.ForeignKey(Booking, related_name="payments", on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
#     paid_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Payment {self.payment_id} for Booking {self.booking.booking_id}"

# class Review(models.Model):
#     review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     property = models.ForeignKey(Property, related_name="reviews", on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
#     rating = models.PositiveSmallIntegerField() # enforce 1-5 in validation
#     comment = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def clean(self):
#         if self.rating < 1 or self.rating > 5:
#             raise ValidationError("Rating must be between 1 and 5") 
        
#     def __str__(self):
#         return f"Review {self.rating}/5 for {self.property.title} by {self.user.email}"
        


