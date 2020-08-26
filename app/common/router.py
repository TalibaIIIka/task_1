import asyncio
import os
from abc import ABC, abstractmethod

import aiostomp

from .settings import get_logger

logger = get_logger('routermq')


class MessageRouter(ABC):
    def __init__(self):
        self._client = aiostomp.AioStomp(
            host=os.environ.get('ACTIVEMQ_HOST'),
            port=int(os.environ.get('ACTIVEMQ_PORT')),
            error_handler=self.on_error
        )
        self._client.subscribe(
            destination=os.environ.get('SOURCE_QUEUE'),
            handler=self.on_message
        )
        self.recipients = os.environ.get('DESTINATION_QUEUES').split(';')
        self._loop = asyncio.get_event_loop()

    @abstractmethod
    async def on_message(self, frame: aiostomp.aiostomp.Frame, message: bytes):
        pass

    async def on_error(self, error):
        logger.error(error)

    async def run(self):
        await self._client.connect()

    def stop(self):
        self._client.close()

    def __repr__(self):
        return f'{self.__class__.__name__}()'
