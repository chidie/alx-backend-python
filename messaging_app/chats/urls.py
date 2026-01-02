from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet, CachedConversationMessagesView

# Main router
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename="user")
router.register(r'conversations', ConversationViewSet, basename="conversation")

# Nested router: messages under conversations
conversation_router = nested_routers.NestedDefaultRouter(
    router, r'conversations', lookup='conversation'
)
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Combine router URLs and custom paths
urlpatterns = [
    # Cached messages view
    path(
        "conversations/<int:conversation_id>/cached-messages/",
        CachedConversationMessagesView.as_view(),
        name="cached-conversation-messages"
    ),
]

# Append router URLs
urlpatterns += router.urls + conversation_router.urls



