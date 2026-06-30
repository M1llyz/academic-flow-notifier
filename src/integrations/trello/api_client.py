import os
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv

from src.models.card import Card


load_dotenv()

TRELLO_API_BASE_URL = "https://api.trello.com/1"
LOCAL_TIMEZONE = ZoneInfo("America/Sao_Paulo")

def format_trello_date(date_value: str | None) -> str:
    """
    Converte a data ISO UTC do Trello para YYYY-MM-DD no fuso do Brasil.
    """

    if not date_value:
        return ""

    utc_datetime = datetime.fromisoformat(date_value.replace("Z", "+00:00"))
    local_datetime = utc_datetime.astimezone(LOCAL_TIMEZONE)

    return local_datetime.date().isoformat()


def get_cards() -> list[Card]:
    """
    Obtém cards reais a partir da API do Trello.
    """

    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")
    board_id = os.getenv("TRELLO_BOARD_ID")

    if not api_key or not token or not board_id:
        raise ValueError("Credenciais do Trello não configuradas no .env")

    url = f"{TRELLO_API_BASE_URL}/boards/{board_id}/cards"

    response = requests.get(
        url,
        params={
            "key": api_key,
            "token": token,
        },
        timeout=30,
    )

    response.raise_for_status()

    cards_data = response.json()

    return [
        Card(
            source_id=item["id"],
            title=item["name"],
            category="",
            description=item.get("desc", ""),
            due_date=format_trello_date(item.get("due")),
            source_url=item.get("url", ""),
        )
        for item in cards_data
        if not item.get("closed", False)
    ]