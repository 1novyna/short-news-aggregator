from django.contrib import admin
from django.utils.html import format_html

from .models import Channel, Message


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ["id", "username_with_url", "messages_number"]

    @admin.display(description="username")
    def username_with_url(self, obj):
        return format_html(
            '<a href="{0}" alt="{1}">{1}</a>',
            obj.get_absolute_url(),
            obj.username,
        )

    username_with_url.allow_tags = True

    @admin.display(description="messages")
    def messages_number(self, obj):
        return obj.messages.count()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "datetime", "message_url"]

    @admin.display(description="message")
    def message_url(self, obj):
        return format_html(
            '<a href="{0}" alt="{0}">{0}</a>',
            obj.get_absolute_url(),
        )

    message_url.allow_tags = True
