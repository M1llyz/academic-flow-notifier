from dataclasses import dataclass

@dataclass
class AcademicEvent:
    event_id: str
    event_type: str
    source: str
    source_id: str
    source_url: str
    title: str
    discipline: str
    category: str
    description: str
    due_date: str
    days_left: int
    priority: str