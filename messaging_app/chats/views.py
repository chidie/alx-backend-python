from django.shortcuts import render
from rest_framework.response import Response
from .models import User, Conversation, Message
from rest_framework import viewsets, status, filters
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .permissions import IsOwner, IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
        return Conversation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        conversation_id = kwargs.get('pk')
        conversation = self.get_object()

        if conversation.user != request.user:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_body"]

    def get_queryset(self):
        return Message.objects.filter(conversation__user=self.request.user) # conversation__participants for many-to-many relationship
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)