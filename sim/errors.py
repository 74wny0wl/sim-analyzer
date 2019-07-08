from dataclasses import dataclass


@dataclass
class LoggableError:
    msg: str
    code: int
