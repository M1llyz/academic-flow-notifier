from src.events.handlers import (
    detect_deadline_events,
    detect_due_date_changed_events,
    detect_new_card_events,
    detect_title_changed_events,
)
from src.integrations.trello.client import get_cards
from src.models.academic_event import AcademicEvent
from src.models.card import Card


def detect_snapshot_events(
    previous_cards: list[Card],
    current_cards: list[Card],
) -> list[AcademicEvent]:
    # Detecta eventos baseados na comparação entre snapshot anterior e estado atual dos cards.

    events: list[AcademicEvent] = []

    events.extend(
        detect_new_card_events(
            previous_cards=previous_cards,
            current_cards=current_cards,
        )
    )

    events.extend(
        detect_due_date_changed_events(
            previous_cards=previous_cards,
            current_cards=current_cards,
        )
    )

    events.extend(
        detect_title_changed_events(
            previous_cards=previous_cards,
            current_cards=current_cards,
        )
    )

    return events


def detect_events(
    current_cards: list[Card],
    previous_cards: list[Card] | None = None,
) -> list[AcademicEvent]:
    """
    Detecta todos os eventos acadêmicos suportados.

    Regra:
    - Cards novos geram apenas NEW_CARD na primeira execução.
    - Lembretes de prazo são gerados apenas para cards já conhecidos.
    """

    events: list[AcademicEvent] = []

    if previous_cards is None:
        events.extend(detect_deadline_events(current_cards))
        return events
    
    snapshot_events = detect_snapshot_events(
        previous_cards=previous_cards,
        current_cards=current_cards,
    )

    events.extend(snapshot_events)

    new_card_source_ids = {
        event.source_id
        for event in snapshot_events
        if event.event_type == "NEW_CARD"
    }

    cards_for_deadline = [
        card
        for card in current_cards
        if card.source_id not in new_card_source_ids
    ]

    events.extend(detect_deadline_events(cards_for_deadline))

    return events


def main():
    cards = get_cards()
    events = detect_events(current_cards=cards)

    print(f"Cards carregados: {len(cards)}")
    print(f"Eventos detectados: {len(events)}")

    for event in events:
        print(
            f"- {event.event_type} | "
            f"{event.title} | "
            f"faltam {event.days_left} dia(s)"
        )


if __name__ == "__main__":
    main()