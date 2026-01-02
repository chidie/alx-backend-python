from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet, InboxView, MarkAsReadView, CachedConversationMessagesView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename="user")
router.register(r'conversations', ConversationViewSet, basename="conversation")

# Nested router for messages inside conversations
conversation_router = nested_routers.NestedDefaultRouter(
    router, 
    r'conversations', 
    lookup='conversation'
)
conversation_router.register(
    r'messages', 
    MessageViewSet, 
    basename='conversation-messages'
)

urlpatterns = [
    path("inbox/", InboxView.as_view(), name="inbox"),
    path("messages/<int:message_id>/read/", MarkAsReadView.as_view(), name="mark-as-read"),
    path(
        "conversations/<int:conversation_id>/cached-messages/",
        CachedConversationMessagesView.as_view(),
        name="cached-conversation-messages"
    ),
]

urlpatterns += router.urls + conversation_router.urls