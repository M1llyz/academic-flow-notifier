from uuid import uuid4

from src.models.academic_event import AcademicEvent
from src.models.notification import Notification
from src.notifications.templates import (
    DEADLINE_SOON_BODY,
    DEADLINE_SOON_SUBJECT,
    DEADLINE_TOMORROW_BODY,
    DEADLINE_TOMORROW_SUBJECT,
    NEW_CARD_BODY,
    NEW_CARD_SUBJECT,
    DUE_DATE_CHANGED_BODY,
    DUE_DATE_CHANGED_SUBJECT,
    TITLE_CHANGED_BODY,
    TITLE_CHANGED_SUBJECT,
)


TEMPLATES = {
    "DEADLINE_SOON": (
        DEADLINE_SOON_SUBJECT,
        DEADLINE_SOON_BODY,
    ),
    "DEADLINE_TOMORROW": (
        DEADLINE_TOMORROW_SUBJECT,
        DEADLINE_TOMORROW_BODY,
    ),
    "NEW_CARD": (
        NEW_CARD_SUBJECT,
        NEW_CARD_BODY,
    ),
    "DUE_DATE_CHANGED": (
        DUE_DATE_CHANGED_SUBJECT,
        DUE_DATE_CHANGED_BODY,
    ),
    "TITLE_CHANGED": (
        TITLE_CHANGED_SUBJECT,
        TITLE_CHANGED_BODY,
    ),
}


def build_notification(event: AcademicEvent) -> Notification:
    """
    Constrói uma Notification a partir de um AcademicEvent.
    """

    if event.event_type not in TEMPLATES:
        raise ValueError(f"Evento não suportado: {event.event_type}")

    subject_template, body_template = TEMPLATES[event.event_type]

    subject = subject_template.format(
        days_left=event.days_left,
    )

    body = body_template.format(
        discipline=event.discipline,
        title=event.title,
        due_date=event.due_date,
        source_url=event.source_url,
        days_left=event.days_left,
    )

    return Notification(
        notification_id=str(uuid4()),
        event_id=event.event_id,
        channel="email",
        subject=subject,
        body=body,
    )