import django_filters
from .models import Conversation, Message

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name="sender__email", lookup_expr='iexact')
    start_time = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'start_time', 'end_time']