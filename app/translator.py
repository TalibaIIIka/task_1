import asyncio
import base64

import aiostomp

from common import MessageRouter, start, get_logger


logger = get_logger()


CHUNK_SIZE = 10240


def chunked_message(message: bytes) -> bytes:
    message_view = memoryview(message)
    while message_view:
        buffer = message_view[:CHUNK_SIZE]
        if len(buffer) < CHUNK_SIZE:
            yield buffer.tobytes()
            return 

        message_view = message_view[len(buffer):]
        yield buffer.tobytes()


class TranslatorRouter(MessageRouter):
    async def on_message(self, frame: aiostomp.aiostomp.Frame, message: bytes):
        if message is None:
            logger.error(f'Empty message: {frame.headers["message-id"]}')
        else:
            decode_message = bytes()
            for chunk in chunked_message(message):
                decode_message += base64.b64decode(chunk)
                await asyncio.sleep(0)

            for channel in self.recipients:
                self._loop.call_soon(self._client.send, channel, decode_message, {})


if __name__ == '__main__':
    message_route = TranslatorRouter()
    start(message_route)
