from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.conf import settings

from telethon.client import TelegramClient

from asgiref.sync import async_to_sync
import json


@require_GET
@async_to_sync
async def get_messages(request):
    channels = request.GET.getlist("channels[]")
    limit = request.GET.get("limit", 10)
    articles = {}
    async with TelegramClient(
        "Gathering articles",
        settings.TELETHON["API_ID"],
        settings.TELETHON["API_HASH"],
    ) as client:
        for name in channels:
            messages = await gather_messages(client, name, limit)
            articles[name] = [serialize_message(obj) for obj in messages]
    data = json.dumps(articles, ensure_ascii=False).encode("utf8")
    return HttpResponse(data, content_type="application/json; charset=utf-8")


async def gather_messages(client, name, limit):
    messages = []
    async for message in client.iter_messages(name, limit=limit):
        messages.append(message)
    return messages


def serialize_message(message):
    return {
        "message": message.message,
        "date": str(message.date),
        "views": message.views,
    }
