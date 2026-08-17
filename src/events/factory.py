from src.models.academic_event import AcademicEvent
from src.models.card import Card


def build_event_id(card: Card, event_type: str) -> str:
    return f"{card.source_id}:{event_type}:{card.due_date}"


def build_event(card: Card, event_type: str, days_left: int) -> AcademicEvent:
    priority = "high" if event_type == "DEADLINE_TOMORROW" else "medium"

    return AcademicEvent(
        event_id=build_event_id(card, event_type),
        event_type=event_type,
        source="trello",
        source_id=card.source_id,
        source_url=card.source_url,
        title=card.title,
        category=card.category,
        description=card.description,
        due_date=card.due_date,
        days_left=days_left,
        priority=priority,
    )