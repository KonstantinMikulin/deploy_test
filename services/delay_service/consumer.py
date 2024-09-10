import logging
from contextlib import suppress
from datetime import datetime, timedelta, timezone

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext

logger = logging.getLogger(__name__)


class DelayedMessageConsumer:
    def __init__(
        self,
        nc: Client,
        js: JetStreamContext,
        bot: Bot,
        subject: str,
        stream: str,
        durable_name: str
    ) -> None:
        self.nc = nc,
        self.js = js,
        self.bot = bot,
        self.subject = subject,
        self.stream = stream,
        self.durable_name = durable_name
        
    async def start(self) -> None:
        self.stream_sub = await self.js.subscribe(
            subject=self.subject,
            stream=self.stream,
            cb=self.on_message,
            durable=self.durable_name,
            manual_ack=True
        )
        
        
