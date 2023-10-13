from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.conf import settings
from asgiref.sync import async_to_sync

from telethon.client import TelegramClient
import json

from groups import group_with_titles


@require_GET
@async_to_sync
async def get_messages(request):
    channels = request.GET.getlist("channels[]")
    limit = int(request.GET.get("limit", "3"))
    messages = []
    async with TelegramClient(
        "Gathering articles",
        settings.TELETHON["API_ID"],
        settings.TELETHON["API_HASH"],
    ) as client:
        for name in channels:
            messages.append(await gather_messages(client, name, limit))
    messages = [data for message in messages for data in message]
    data = json.dumps(group_with_titles(messages, 2), ensure_ascii=False).encode("utf8")
    return HttpResponse(data, content_type="application/json; charset=utf-8")


async def gather_messages(client, name, limit):
    messages = []
    async for message in client.iter_messages(name, limit=limit):
        messages.append(clear_message(message))
    return messages


def clear_message(message):
    return message.message
