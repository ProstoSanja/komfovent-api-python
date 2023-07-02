from enum import Enum


class KomfoventConnectionResult(Enum):
    SUCCESS = 1
    NOT_FOUND = 2
    UNAUTHORISED = 3