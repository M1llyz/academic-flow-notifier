from src.workflows.flow_notifier import run_flow


def main():
    print("===== Academic Flow Notifier =====\n")

    result = run_flow()

    cards = result["cards"]
    events = result["events"]
    notifications = result["notifications"]

    print(f"Cards carregados: {len(cards)}")
    print(f"Eventos detectados: {len(events)}")
    print(f"Notificações geradas: {len(notifications)}")
    print("Snapshot atualizado.")

    if not notifications:
        print("\nNenhuma notificação gerada nesta execução.")
        return

    print("\n===== Notificações =====\n")

    for notification in notifications:
        print(f"Assunto: {notification.subject}")
        print(notification.body)
        print("-" * 50)


if __name__ == "__main__":
    main()