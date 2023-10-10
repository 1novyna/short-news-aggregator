from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.conf import settings

from telethon.client import TelegramClient

from asgiref.sync import async_to_sync
import json

from keywords.groupping import group_by_keywords
from keywords.clearing import clear_text


@require_GET
@async_to_sync
async def get_messages(request):
    channels = request.GET.getlist("channels[]")
    limit = request.GET.get("limit", 10)
    async with TelegramClient(
        "Gathering articles",
        settings.TELETHON["API_ID"],
        settings.TELETHON["API_HASH"],
    ) as client:
        for name in channels:
            messages = await gather_messages(client, name, limit)
    data = json.dumps(group_by_keywords(messages), ensure_ascii=False).encode("utf8")
    return HttpResponse(data, content_type="application/json; charset=utf-8")


async def gather_messages(client, name, limit):
    messages = []
    async for message in client.iter_messages(name, limit=limit):
        messages.append(message)
    return clear_messages(messages)


def clear_messages(messages):
    result = []
    for message in messages:
        if message.message:
            result.append(clear_text(message.message))
    return result
