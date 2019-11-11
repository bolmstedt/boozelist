"""Service description."""
from typing import List

import sentry_sdk

from app.configuration import CONFIG, SENTRY_DISABLED
from thread_runner import Runnable, ThreadRunner


def _main() -> None:
    if CONFIG.sentry_dsn != SENTRY_DISABLED:
        sentry_sdk.init(CONFIG.sentry_dsn)

    services: List[Runnable] = [
        # Your runnable services here
    ]

    ThreadRunner(services).run()


if __name__ == "__main__":
    _main()
