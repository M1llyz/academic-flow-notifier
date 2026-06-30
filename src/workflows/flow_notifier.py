from src.events.detector import detect_events
from src.integrations.trello.client import get_cards
from src.notifications.builder import build_notification
from src.outputs.json_exporter import export_notifications
from src.persistence.state_store import (
    load_snapshot,
    save_snapshot,
)


def run_flow():
    """
    Executa todo o fluxo principal da aplicação.
    """

    current_cards = get_cards()
    previous_cards = load_snapshot()

    events = detect_events(
        current_cards=current_cards,
        previous_cards=previous_cards,
    )

    notifications = [
        build_notification(event)
        for event in events
    ]

    export_notifications(notifications)

    save_snapshot(current_cards)

    return {
        "cards": current_cards,
        "events": events,
        "notifications": notifications,
    }