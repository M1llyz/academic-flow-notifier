from datetime import date, datetime

def calculate_days_left(due_date: str, reference_date: date | None = None) -> int:
    """
    Calcula quantos dias faltam até a data de vencimento.

    due_date deve estar no formato YYYY-MM-DD.
    reference_date permite simular uma data atual durante testes.
    """

    if reference_date is None:
        reference_date = date.today()

    due = datetime.strptime(due_date, "%Y-%m-%d").date()

    return (due - reference_date).days

if __name__ == "__main__":
    days = calculate_days_left("2026-08-20")
    print(f"Dias restantes: {days}")