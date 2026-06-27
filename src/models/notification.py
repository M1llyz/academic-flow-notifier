from dataclasses import dataclass

@dataclass
class Notification:
    notification_id: str
    event_id: str
    channel: str
    subject: str
    body: str
    status: str = "PENDING"