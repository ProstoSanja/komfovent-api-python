from enum import Enum
from urllib.parse import urlparse, ParseResult


class KomfoventConnectionResult(Enum):
    SUCCESS = 1
    NOT_FOUND = 2
    UNAUTHORISED = 3
    INVALID_INPUT = 4

class KomfoventCredentials():
  
    __host: ParseResult = None
    username = None
    password = None

    def __init__(self, host: str, username: str, password: str):
        if "://" in host:
            self.__host = urlparse(host)
        else:
            self.__host = urlparse("//" + host)
        self.username = username
        self.password = password

    def host(self) -> str:
        return "http://" + self.__host.netloc