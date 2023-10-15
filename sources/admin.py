from django.contrib import admin

from commons.admin import ExternalLinkTag

from .models import Channel, Message
from .forms import ChannelForm


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username_with_url",
        "channel_id",
        "messages_number",
    ]
    form = ChannelForm

    username_with_url = admin.display(
        ExternalLinkTag(
            href="get_absolute_url",
            alt="username",
            inner_text="username",
            open_new_tab=True,
        ),
        description="username",
    )

    @admin.display(description="messages")
    def messages_number(self, obj):
        return obj.messages.count()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "datetime",
        "message_url",
        "is_embedded",
    ]

    message_url = admin.display(
        ExternalLinkTag(
            href="get_absolute_url",
            alt="__str__",
            inner_text="get_absolute_url",
            open_new_tab=True,
        ),
        description="message",
    )

    @admin.display(description="is embedded")
    def is_embedded(self, obj):
        return obj.embedding != None
