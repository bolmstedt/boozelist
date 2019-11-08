"""Loads configuration from ENV, using defaults from a NamedTuple."""
import dataclasses
import typing
import os


def load(definition: typing.Type[object]) -> typing.List[typing.Any]:
    if not dataclasses.is_dataclass(definition):
        raise TypeError('{} is not a dataclass'.
                        format(type(definition).__name__))

    return [_cast(os.getenv(field.name.upper(), field.default), field.type)
            for field in dataclasses.fields(definition)]


def _cast(value, to_type):
    if to_type == type(value):
        return value
    if type(value) == str:
        if to_type == bool:
            return value.lower() in ['true', '1']
        if to_type == list:
            return [v.strip() for v in value.split(',')]

    return to_type(value)
