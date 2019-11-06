"""Provides the Runnable class stub and ThreadRunner class."""
import threading
import typing


class Runnable:
    def run(self):
        raise NotImplementedError


class ThreadRunner:
    """Runs as set of services in threads."""

    def __init__(self, services: typing.List[Runnable]) -> None:
        self.services = services

    def run(self):
        """Run services in threads."""
        threads = []

        for service in self.services:
            threads.append(threading.Thread(target=service.run))

        for thread in threads:
            thread.start()
