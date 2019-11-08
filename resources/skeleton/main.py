"""Service description."""
from typing import List

from app.configuration import CONFIG
from thread_runner import ThreadRunner, Runnable


def _main() -> None:
    services: List[Runnable] = [
        # Your runnable services here
    ]

    ThreadRunner(services).run()


if __name__ == "__main__":
    _main()
