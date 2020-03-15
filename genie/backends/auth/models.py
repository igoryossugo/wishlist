from dataclasses import dataclass


@dataclass
class Application:
    name: str
    active: bool
