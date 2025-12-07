from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "first_name", "last_name", "email", "phone_number", "role", "created_at"]

# class PropertySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Property
#         fields = "__all__"

# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = "__all__"
    
# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = "__all__"

# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["message_id", "conversation", "sender", "message_body", "sent_at"]

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source="messages")
    participant_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "created_at", "messages"]
    
    def get_participant_count(self, obj):
        return obj.participants.count()
    
