from src.models.card import Card


def index_cards_by_id(cards: list[Card]) -> dict[str, Card]:
    """
    Cria um dicionário usando source_id como chave.
    Facilita comparar cards antigos e atuais.
    """

    return {card.source_id: card for card in cards}


def find_new_cards(
    previous_cards: list[Card],
    current_cards: list[Card],
) -> list[Card]:
    """
    Identifica cards que existem no estado atual,
    mas não existiam no snapshot anterior.
    """

    previous_by_id = index_cards_by_id(previous_cards)

    return [
        card
        for card in current_cards
        if card.source_id not in previous_by_id
    ]


def find_due_date_changes(
    previous_cards: list[Card],
    current_cards: list[Card],
) -> list[tuple[Card, Card]]:
    """
    Identifica cards cujo prazo foi alterado.

    Retorna uma lista de tuplas:
    (card_anterior, card_atual)
    """

    previous_by_id = index_cards_by_id(previous_cards)

    changes = []

    for current_card in current_cards:
        previous_card = previous_by_id.get(current_card.source_id)

        if previous_card is None:
            continue

        if previous_card.due_date != current_card.due_date:
            changes.append((previous_card, current_card))

    return changes

def find_title_changes(
    previous_cards: list[Card],
    current_cards: list[Card],
) -> list[tuple[Card, Card]]:
    """
    Identifica cards cujo título foi alterado.

    Retorna uma lista de tuplas:
    (card_anterior, card_atual)
    """

    previous_by_id = index_cards_by_id(previous_cards)

    changes = []

    for current_card in current_cards:
        previous_card = previous_by_id.get(current_card.source_id)

        if previous_card is None:
            continue

        if previous_card.title != current_card.title:
            changes.append((previous_card, current_card))

    return changes