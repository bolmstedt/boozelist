"""Loads configuration from ENV, using defaults from a NamedTuple."""
import typing
import os


def load(definition: typing.Type[typing.NamedTuple]) -> list:
    """Use with a NamedTuple and expand list with *."""
    return [_cast(os.getenv(k.upper(), definition._field_defaults.get(k)),
                  definition._field_types.get(k))
            for k in definition._fields]


def _cast(value, to_type):
    if to_type == type(value):
        return value
    if type(value) == str:
        if to_type == bool:
            return value.lower() in ['true', '1']
        if to_type == list:
            return [v.strip() for v in value.split(',')]

    return to_type(value)
