import json
from pathlib import Path

from src.models.card import Card


SNAPSHOT_FILE = Path("data/snapshots/current_snapshot.json")


def card_to_dict(card: Card) -> dict:
    """
    Converte um Card em dicionário para persistência em JSON.
    """

    return {
        "source_id": card.source_id,
        "title": card.title,
        "discipline": card.discipline,
        "category": card.category,
        "description": card.description,
        "due_date": card.due_date,
        "source_url": card.source_url,
    }


def dict_to_card(data: dict) -> Card:
    """
    Converte um dicionário salvo em JSON para um Card.
    """

    return Card(
        source_id=data["source_id"],
        title=data["title"],
        discipline=data["discipline"],
        category=data["category"],
        description=data["description"],
        due_date=data["due_date"],
        source_url=data["source_url"],
    )


def save_snapshot(cards: list[Card], file_path: Path = SNAPSHOT_FILE) -> None:
    """
    Salva o estado atual dos cards em um arquivo JSON.
    """

    file_path.parent.mkdir(parents=True, exist_ok=True)

    cards_data = [card_to_dict(card) for card in cards]

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(cards_data, file, ensure_ascii=False, indent=2)


def load_snapshot(file_path: Path = SNAPSHOT_FILE) -> list[Card]:
    """
    Carrega o último snapshot salvo.

    Se ainda não existir snapshot, retorna uma lista vazia.
    """

    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        cards_data = json.load(file)

    return [dict_to_card(item) for item in cards_data]
