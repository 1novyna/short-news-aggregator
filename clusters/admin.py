from django.contrib import admin

from telegram_messages.models import Message

from .models import Cluster


class MessageInline(admin.TabularInline):
    model = Message


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "digest",
        "messages_number",
    ]
    inlines = [
        MessageInline,
    ]

    @admin.display(description="messages")
    def messages_number(self, obj):
        return obj.messages.count()
