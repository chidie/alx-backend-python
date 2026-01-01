from django.contrib import admin
from .models import User, Conversation, Message, Notification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "role", "created_at")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("role",)

# @admin.register(Property)
# class PropertyAdmin(admin.ModelAdmin):
#     list_display = ("title", "location", "host", "price_per_night", "created_at")
#     search_fields = ("title", "location")

# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ("property", "user", "status", "check_in", "check_out", "created_at")
#     list_filter = ("status",)

# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ("booking", "amount", "paid_at")

# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ("property", "user", "rating", "created_at")
#     list_filter = ("rating",)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("conversation_id", "created_at")
    filter_horizontal = ("participants",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message_id", "sender", "receiver", "content", "conversation", "timestamp") 
    list_filter = ("sender", "receiver", "content", "conversation", "timestamp") 
    search_fields = ("content", "sender__email", "receiver__email")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "is_read", "created_at")
    list_filter = ("is_read", "created_at", "user")
    search_fields = ("user__email", "message__message_body")