from dataclasses import dataclass


@dataclass
class Notification:
    notification_id: str
    event_id: str
    event_type: str
    activity_title: str
    due_date: str
    source_url: str
    channel: str
    subject: str
    body: str
    body_html: str
    body_text: str
    requires_approval: bool
    status: str