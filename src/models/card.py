from dataclasses import dataclass

@dataclass
class Card:
    source_id: str
    title: str
    discipline: str
    category: str
    description: str
    due_date: str
    source_url: str