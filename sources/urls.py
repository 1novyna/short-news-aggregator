from django.urls import path

from .views import get_messages
from .apps import SourcesConfig

app_name = SourcesConfig.name

urlpatterns = [
    path("messages/", get_messages, name="messages"),
]
