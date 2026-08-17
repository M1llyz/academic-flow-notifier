AUTOMATIC_EVENTS = {
    "DEADLINE_SOON",
    "DEADLINE_TOMORROW",
}

def get_approval_rule(event_type: str) -> tuple[bool, str]:
    """
    Define se uma notificação precisa de aprovação humana
    e qual deve ser seu status inicial.
    """

    if event_type in AUTOMATIC_EVENTS:
        return False, "READY_TO_SEND"

    return True, "PENDING_APPROVAL"