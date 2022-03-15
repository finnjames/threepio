from dataclasses import dataclass


@dataclass()
class AlertMessage:
    alert: str
    alert_button: str = "Close"
    confirmation: str = "Confirm?"
    confirmation_button: str = "Yes"
