import asyncio
import signal
from contextlib import suppress

from .router import MessageRouter

from .settings import get_logger

logger = get_logger()


def start(router: MessageRouter):
    loop = asyncio.get_event_loop()

    graceful_shutdown(loop, router)

    loop.run_until_complete(router.run())
    loop.run_forever()


async def ask_exit(router: MessageRouter):
    router.stop()
    logger.warning(f'{router} was stopped')

    pending = [t for t in asyncio.Task.all_tasks() if t is not asyncio.current_task()]
    for task in pending:
        task.cancel()
    with suppress(asyncio.CancelledError):
        await asyncio.gather(*pending)


def graceful_shutdown(loop, router: MessageRouter):
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            lambda: asyncio.create_task(ask_exit(router))
        )
