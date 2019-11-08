"""Provides the Runnable class stub and ThreadRunner class."""
import signal
import threading
import time
import typing


class Runner:
    run = True

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame) -> None:
        self.run = False


class Runnable:
    """Runnable class for threading, with injected helper for stopping."""

    DAEMON = False

    def run(self, runner: Runner) -> None:
        raise NotImplementedError


class ThreadRunner:
    """Runs as set of services in threads."""

    def __init__(self, services: typing.List[Runnable]) -> None:
        self.services = services

    def run(self) -> None:
        """Run services in threads."""
        threads = []
        runner = Runner()

        for service in self.services:
            threads.append(threading.Thread(
                target=service.run,
                args=(runner,),
                daemon=service.DAEMON
            ))

        for thread in threads:
            thread.start()
