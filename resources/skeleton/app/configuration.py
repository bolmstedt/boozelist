"""Contains configuration for this application."""
from dataclasses import dataclass

import config

# Define config constants below.
# Example: GLOBAL_CONF = 'some_value'


@dataclass(frozen=True)
class ConfigDefinition:
    """Definition of config parameters.

    Should have entries like this:
    int_var: int
    str_var: str = 'default_value'
    """


# Import ENV variables and cast them to override default values.
CONFIG = ConfigDefinition(*config.load(ConfigDefinition))
