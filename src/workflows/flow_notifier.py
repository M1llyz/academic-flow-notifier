from src.events.detector import detect_events
from src.integrations.trello.client import get_cards
from src.notifications.builder import build_notification
from src.outputs.json_exporter import export_notifications
from src.persistence.state_store import (
    filter_unprocessed_events,
    load_processed_events,
    load_snapshot,
    save_processed_events,
    save_snapshot,
)


def run_flow():
    """
    Executa todo o fluxo principal da aplicação.
    """

    current_cards = get_cards()
    previous_cards = load_snapshot()
    processed_event_ids = load_processed_events()

    events = detect_events(
        current_cards=current_cards,
        previous_cards=previous_cards,
    )

    unprocessed_events = filter_unprocessed_events(
        events=events,
        processed_event_ids=processed_event_ids,
    )

    notifications = [
        build_notification(event)
        for event in unprocessed_events
    ]

    export_notifications(notifications)

    processed_event_ids.update(
        event.event_id
        for event in unprocessed_events
    )

    save_processed_events(processed_event_ids)
    save_snapshot(current_cards)

    return {
        "cards": current_cards,
        "events": events,
        "unprocessed_events": unprocessed_events,
        "notifications": notifications,
    }