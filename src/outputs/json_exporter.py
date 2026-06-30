import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


from src.models.notification import Notification


OUTPUT_FILE = Path("data/outputs/notifications.json")
LOCAL_TIMEZONE = ZoneInfo("America/Sao_Paulo")


def export_notifications(notifications: list[Notification]) -> None:
    """
    Exporta as notificações geradas para um arquivo JSON.
    """

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(LOCAL_TIMEZONE).isoformat()

    payload = {
        "generated_at": generated_at,
        "notifications_count": len(notifications),
        "notifications": [
            {
                "notification_id": notification.notification_id,
                "event_id": notification.event_id,
                "channel": notification.channel,
                "subject": notification.subject,
                "body": notification.body,
                "status": "PENDING",
            }
            for notification in notifications
        ],
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            payload,
            file,
            ensure_ascii=False,
            indent=4,
        )