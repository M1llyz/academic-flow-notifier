import os

from dotenv import load_dotenv

from src.integrations.trello.api_client import get_cards as get_api_cards
from src.integrations.trello.mock_client import get_cards as get_mock_cards
from src.models.card import Card


load_dotenv()


def get_cards() -> list[Card]:
    """
    Seleciona a fonte de dados dos cards conforme DATA_SOURCE.
    """

    data_source = os.getenv("DATA_SOURCE", "mock")

    if data_source == "mock":
        return get_mock_cards()

    if data_source == "trello":
        return get_api_cards()

    raise ValueError(f"DATA_SOURCE inválido: {data_source}")