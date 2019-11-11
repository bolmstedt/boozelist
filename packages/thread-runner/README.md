# Thread Runner

Provides the Runnable class stub and ThreadRunner class.

Injects a Runner instance into each Runnable `run()` method to be used for graceful shutdown.

## Usage

In your `main.py`, import the Thread Runner with `from `

```python
from typing import List

from thread_runner import Runnable, ThreadRunner

services: List[Runnable] = [
    # Your runnable instances here
]

ThreadRunner(services).run()
```

Create one or more Runnable classes:

```python
from thread_runner import Runnable, Runner

class MyClass(Runnable):
    def run(self, runner: Runner) -> None:
        while runner.run:
            # Do your logic
            pass
        
        # Handle shutdown
```