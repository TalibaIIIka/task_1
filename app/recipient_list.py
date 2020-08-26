import aiostomp

from common import MessageRouter, start, get_logger


logger = get_logger()


class RecipientsRouter(MessageRouter):
    async def on_message(self, frame: aiostomp.aiostomp.Frame, message: bytes):
        if message is None:
            logger.error(f'Empty message: {frame.headers["message-id"]}')
        else:
            for channel in self.recipients:
                self._loop.call_soon(self._client.send, channel, message, {})


if __name__ == '__main__':
    message_route = RecipientsRouter()
    start(message_route)
