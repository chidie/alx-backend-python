from django.shortcuts import render
from rest_framework.response import Response
from .models import User, Conversation, Message
from rest_framework import viewsets, status, filters
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .permissions import IsOwner, IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from .pagination import MessagePagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner] # Only authenticated users can access user data or [IsAdminUser] for admin only
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "email"]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        # Return only conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Create the conversation with no participants yet
        conversation = serializer.save()
        # Add the creator as the first participant
        conversation.participants.add(self.request.user)

    def retrieve(self, request, *args, **kwargs):
        conversation_id = kwargs.get("pk")

        # Ensure the conversation exists AND the user is a participant
        try:
            conversation = self.get_queryset().get(pk=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(conversation)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet): 
    serializer_class = MessageSerializer 
    
    def get_queryset(self): 
        return Message.objects.filter(
            conversation_id=self.kwargs["conversation_pk"],
            conversation__participants=self.request.user
        )
    
    def perform_create(self, serializer): 
        conversation = Conversation.objects.get(
            pk=self.kwargs["conversation_pk"]
        )

        parent_id = self.request.data.get("parent_message")
        parent = None

        if parent_id:
            parent = Message.objects.filter(
                id=parent_id,
                conversation=conversation
            ).first()
            
        serializer.save(
            sender=self.request.user,
            conversation=conversation,
            parent_message=parent
        )
        conversation.participants.add(self.request.user)
    
    def list(self, request, *args, **kwargs):
        conversation_id = self.kwargs["conversation_pk"]

        messages = (
            Message.objects
            .filter(conversation_id=conversation_id, parent_message__isnull=True)
            .select_related("sender", "receiver", "parent_message")
            .prefetch_related("replies")
            .order_by("timestamp")
        )

        from .threading import build_thread

        threaded = [build_thread(m) for m in messages]

        return Response(threaded)


@api_view(['DELETE'])
def delete_user(request):
    user = request.user

    if not user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
    
    user.delete()
    return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)