from html import escape

EVENT_MESSAGES = {
    "DEADLINE_TOMORROW": {
        "intro": "A atividade abaixo vence amanhã.",
        "closing": "Não deixe para a última hora!",
    },
    "DEADLINE_SOON": {
        "intro": "Este é um lembrete de que a atividade abaixo está próxima do prazo de entrega.",
        "closing": "Bom estudo!",
    },
    "NEW_CARD": {
        "intro": "Uma nova atividade foi adicionada ao cronograma acadêmico.",
        "closing": "Fique atento(a) às próximas atualizações!",
    },
    "DUE_DATE_CHANGED": {
        "intro": "O prazo de uma atividade foi atualizado no cronograma acadêmico.",
        "closing": "Confira a alteração para se organizar direitinho.",
    },
    "TITLE_CHANGED": {
        "intro": "O título de uma atividade foi atualizado no cronograma acadêmico.",
        "closing": "Confira a atualização no Trello para evitar confusão.",
    },
}


def build_notification_content_html(
    event_type: str,
    title: str,
    due_date: str,
    source_url: str,
) -> str:
    message = EVENT_MESSAGES[event_type]

    return f"""
<p class="intro">Olá!</p>

<p>{escape(message["intro"])}</p>

<div class="activity-card">
    <div class="field">
        <span class="label">📝 Atividade</span>
        <span class="value">{escape(title)}</span>
    </div>
    
    <div class="field">
        <span class="label">📅 Prazo</span>
        <span class="value">{escape(due_date)}</span>
    </div>

    <p class="button-description">
        Acesse abaixo o cronograma completo para consultar a descrição, anexos e mais informações da atividade.
    </p>

    <a class="button" href="{escape(source_url)}" target="_blank">
        🔗 Ver atividade no Trello
    </a>
</div>

<p>{escape(message["closing"])}</p>
"""


def build_notification_content_text(
    event_type: str,
    title: str,
    due_date: str,
    source_url: str,
) -> str:
    message = EVENT_MESSAGES[event_type]

    return f"""Olá!

{message["intro"]}

Atividade:
{title}

Prazo:
{due_date}

Acesse o cronograma completo:
{source_url}

{message["closing"]}
"""