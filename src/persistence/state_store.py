import json
from pathlib import Path

from src.models.card import Card


SNAPSHOT_FILE = Path("data/snapshots/current_snapshot.json")
PROCESSED_EVENTS_FILE = Path("data/state/processed_events.json")


def card_to_dict(card: Card) -> dict:
    return {
        "source_id": card.source_id,
        "title": card.title,
        "category": card.category,
        "description": card.description,
        "due_date": card.due_date,
        "source_url": card.source_url,
    }


def dict_to_card(data: dict) -> Card:
    return Card(
        source_id=data["source_id"],
        title=data["title"],
        category=data.get("category", ""),
        description=data.get("description", ""),
        due_date=data.get("due_date", ""),
        source_url=data.get("source_url", ""),
    )


def save_snapshot(cards: list[Card], file_path: Path = SNAPSHOT_FILE) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)

    cards_data = [card_to_dict(card) for card in cards]

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(cards_data, file, ensure_ascii=False, indent=2)


def load_snapshot(file_path: Path = SNAPSHOT_FILE) -> list[Card]:
    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        cards_data = json.load(file)

    return [dict_to_card(item) for item in cards_data]


def load_processed_events(file_path: Path = PROCESSED_EVENTS_FILE) -> set[str]:
    if not file_path.exists():
        return set()

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return set(data.get("processed_event_ids", []))


def save_processed_events(
    processed_event_ids: set[str],
    file_path: Path = PROCESSED_EVENTS_FILE,
) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "processed_event_ids": sorted(processed_event_ids),
    }

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def filter_unprocessed_events(events, processed_event_ids: set[str]):
    return [
        event
        for event in events
        if event.event_id not in processed_event_ids
    ]