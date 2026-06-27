import json

from src.models.card import Card

MOCK_CARDS_FILE = "data/fixtures/mock_cards.json"


def get_cards(file_path: str = MOCK_CARDS_FILE) -> list[Card]:
    """
    Obtém a lista de cards do Trello.

    Atualmente utiliza um arquivo JSON para simular a resposta da API.
    Futuramente esta função será responsável por consumir a Trello API
    e retornar os cards já normalizados para o restante da aplicação.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        cards_data = json.load(file)

    return [
        Card(
            source_id=item["source_id"],
            title=item["title"],
            discipline=item["discipline"],
            category=item["category"],
            description=item["description"],
            due_date=item["due_date"],
            source_url=item["source_url"],
        )
        for item in cards_data
    ]