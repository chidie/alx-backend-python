from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename="user")
# router.register(r'properties', PropertyViewSet, basename="property")
# router.register(r'bookings', BookingViewSet, basename="booking")
# router.register(r'payments', PaymentViewSet, basename="payment")
# router.register(r'reviews', ReviewViewSet, basename="review")
router.register(r'conversations', ConversationViewSet, basename="conversation")
router.register(r'messages', MessageViewSet, basename="message")
urlpatterns = router.urls
# urlpatterns = [
#     path("api/", include(router.urls)),
# ]