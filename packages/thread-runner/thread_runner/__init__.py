"""Provides the Runnable class stub and ThreadRunner class."""
import signal
import threading
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
        self.threads = []

    def run(self) -> None:
        """Run services in threads."""
        runner = Runner()

        for service in self.services:
            threading.Thread(
                name=type(service).__name__,
                target=service.run,
                args=(runner,),
                daemon=service.DAEMON
            ).start()
