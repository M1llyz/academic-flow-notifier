import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from src.models.notification import Notification

OUTPUT_FILE = Path("data/outputs/notifications.json")
LOCAL_TIMEZONE = ZoneInfo("America/Sao_Paulo")


def export_notifications(notifications: list[Notification]) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(LOCAL_TIMEZONE).isoformat()

    payload = {
        "generated_at": generated_at,
        "notifications_count": len(notifications),
        "notifications": [
            {
                "notification_id": notification.notification_id,
                "event_id": notification.event_id,
                "event_type": notification.event_type,
                "activity_title": notification.activity_title,
                "due_date": notification.due_date,
                "source_url": notification.source_url,
                "channel": notification.channel,
                "subject": notification.subject,
                "body": notification.body,
                "body_html": notification.body_html,
                "body_text": notification.body_text,
                "requires_approval": notification.requires_approval,
                "status": notification.status,
            }
            for notification in notifications
        ],
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=4)