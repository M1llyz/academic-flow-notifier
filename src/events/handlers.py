from src.events.classifier import calculate_days_left
from src.events.comparator import (
    find_due_date_changes,
    find_new_cards,
    find_title_changes,
)
from src.events.factory import build_event
from src.models.academic_event import AcademicEvent
from src.models.card import Card


def detect_deadline_events(cards: list[Card]) -> list[AcademicEvent]:
    """
    Detecta eventos baseados na proximidade do prazo.
    Cards sem data de vencimento são ignorados.
    """

    events: list[AcademicEvent] = []

    for card in cards:
        if not card.due_date:
            continue

        days_left = calculate_days_left(card.due_date)

        if days_left == 3:
            events.append(
                build_event(
                    card=card,
                    event_type="DEADLINE_SOON",
                    days_left=days_left,
                )
            )

        elif days_left == 1:
            events.append(
                build_event(
                    card=card,
                    event_type="DEADLINE_TOMORROW",
                    days_left=days_left,
                )
            )

    return events


def detect_new_card_events(
    previous_cards: list[Card],
    current_cards: list[Card],
) -> list[AcademicEvent]:
    """
    Detecta novos cards adicionados ao cronograma.
    """

    events: list[AcademicEvent] = []

    new_cards = find_new_cards(
        previous_cards=previous_cards,
        current_cards=current_cards,
    )

    for card in new_cards:
        days_left = calculate_days_left(card.due_date) if card.due_date else -1

        events.append(
            build_event(
                card=card,
                event_type="NEW_CARD",
                days_left=days_left,
            )
        )

    return events


def detect_due_date_changed_events(
    previous_cards: list[Card],
    current_cards: list[Card],
) -> list[AcademicEvent]:
    """
    Detecta cards cujo prazo foi alterado.
    """

    events: list[AcademicEvent] = []

    due_date_changes = find_due_date_changes(
        previous_cards=previous_cards,
        current_cards=current_cards,
    )

    for previous_card, current_card in due_date_changes:
        days_left = (
            calculate_days_left(current_card.due_date)
            if current_card.due_date
            else -1
        )

        events.append(
            build_event(
                card=current_card,
                event_type="DUE_DATE_CHANGED",
                days_left=days_left,
            )
        )

    return events


def detect_title_changed_events(
    previous_cards: list[Card],
    current_cards: list[Card],
) -> list[AcademicEvent]:
    """
    Detecta cards cujo título foi alterado.
    """

    events: list[AcademicEvent] = []

    title_changes = find_title_changes(
        previous_cards=previous_cards,
        current_cards=current_cards,
    )

    for previous_card, current_card in title_changes:
        days_left = calculate_days_left(current_card.due_date) if current_card.due_date else -1

        events.append(
            build_event(
                card=current_card,
                event_type="TITLE_CHANGED",
                days_left=days_left,
            )
        )

    return events