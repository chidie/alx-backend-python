from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet

router = routers.DefaultRouter() # routers.SimpleRouter()
router.register(r'users', UserViewSet, basename="user")
# router.register(r'properties', PropertyViewSet, basename="property")
# router.register(r'bookings', BookingViewSet, basename="booking")
# router.register(r'payments', PaymentViewSet, basename="payment")
# router.register(r'reviews', ReviewViewSet, basename="review")
router.register(r'conversations', ConversationViewSet, basename="conversation")
# router.register(r'messages', MessageViewSet, basename="message")

# Nested router: messages under conversations
conversation_router = nested_routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')
urlpatterns = router.urls + conversation_router.urls






