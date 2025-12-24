from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants (authenticated users) of a conversation to access it.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated globally.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission to check if the user is a participant of the conversation.
        """
        user = request.user

        # If the object is a conversation, check if the user is a participant
        if hasattr(obj, "participants"):
            return user in obj.participants.all()
        
        # If the object is a Message
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants.all()
        
        return False

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access or edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the object's owner is the same as the requesting user
        return obj.owner == request.user