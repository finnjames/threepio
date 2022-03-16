from dataclasses import dataclass


@dataclass()
class Alert:
    text: str
    button: str = "Close"
