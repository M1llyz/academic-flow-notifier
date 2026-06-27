DEADLINE_SOON_SUBJECT = (
    "⏰ Lembrete: faltam {days_left} dias para a entrega da atividade"
)

DEADLINE_SOON_BODY = """
Olá!

Este é um lembrete de que a atividade abaixo está próxima do prazo de entrega.

📚 Disciplina:
{discipline}

📝 Atividade:
{title}

📅 Prazo:
{due_date}

🔗 Acesse o cronograma:
{source_url}

Bom estudo!
"""

DEADLINE_TOMORROW_SUBJECT = (
    "🚨 Atenção: a atividade vence amanhã"
)

DEADLINE_TOMORROW_BODY = """
Olá!

A atividade abaixo vence amanhã.

📚 Disciplina:
{discipline}

📝 Atividade:
{title}

📅 Prazo:
{due_date}

🔗 Acesse o cronograma:
{source_url}

Não deixe para a última hora!
"""

NEW_CARD_SUBJECT = "📌 Nova atividade adicionada ao cronograma"

NEW_CARD_BODY = """
Olá!

Uma nova atividade foi adicionada ao cronograma acadêmico.

📚 Disciplina:
{discipline}

📝 Atividade:
{title}

📅 Prazo:
{due_date}

🔗 Acesse o cronograma:
{source_url}

Fique atento(a) às próximas atualizações!
"""

DUE_DATE_CHANGED_SUBJECT = "🔄 Prazo atualizado no cronograma"

DUE_DATE_CHANGED_BODY = """
Olá!

O prazo de uma atividade foi atualizado no cronograma acadêmico.

📚 Disciplina:
{discipline}

📝 Atividade:
{title}

📅 Novo prazo:
{due_date}

🔗 Acesse o cronograma:
{source_url}

Confira a alteração para se organizar direitinho.
"""

TITLE_CHANGED_SUBJECT = "✏️ Atividade atualizada no cronograma"

TITLE_CHANGED_BODY = """
Olá!

Uma atividade teve o título atualizado no cronograma acadêmico.

📚 Disciplina:
{discipline}

📝 Atividade atualizada:
{title}

📅 Prazo:
{due_date}

🔗 Acesse o cronograma:
{source_url}

Confira a atualização para evitar confusão.
"""