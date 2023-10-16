from django.conf import settings

from telethon.client import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from sources.models import Channel, Message


async def gather_messages():
    async with TelegramClient(
        "Gathering messages",
        settings.TELETHON["API_ID"],
        settings.TELETHON["API_HASH"],
    ) as client:
        async for channel in Channel.objects.all():
            recent_message = await channel.messages.order_by("-datetime").afirst()
            message_id = recent_message.message_id if recent_message else 0
            telegram_messages = await get_new_messages(
                client,
                channel.username,
                message_id,
            )
            await save_telegram_messages(telegram_messages.messages)


async def save_telegram_messages(messages):
    result = await Message.objects.abulk_create(
        [
            Message(
                message_id=obj.id,
                channel=await Channel.objects.aget(channel_id=obj.peer_id.channel_id),
                text=obj.message,
                datetime=obj.date,
            )
            for obj in messages
            if obj.message
        ]
    )
    return result


async def get_new_messages(client, username, recent_message_id):
    channel = await client.get_entity(username)
    optional_kwargs = {
        "offset_id": 0,
        "offset_date": None,
        "add_offset": 0,
        "max_id": 0,
        "hash": 0,
    }
    messages = await client(
        GetHistoryRequest(
            peer=channel,
            limit=100,
            min_id=recent_message_id,
            **optional_kwargs,
        )
    )
    return messages
