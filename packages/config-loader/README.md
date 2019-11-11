# Config Loader

Loads configuration from `ENV`, using defaults from a dataclass.

## Usage

Add a Python file in your `app` directory called `configuration.py` and add the following:

```python
from dataclasses import dataclass

import config

@dataclass(frozen=True)
class ConfigDefinition:
    """Definition of config parameters.

    Should have entries like this:
    int_var: int
    str_var: str = 'default_value'
    """


# Import ENV variables and cast them to override default values.
CONFIG = ConfigDefinition(*config.load(ConfigDefinition))
```

Then use it in your `main.py` like `CONFIG.setting` by importing `CONFIG` as `from app.configuration import CONFIG`.
