try:
    from plyer import notification

    def notify(title: str, message: str):
        try:
            notification.notify(title=title, message=message, timeout=5)
        except Exception:
            print(f"{title}: {message}")
except Exception:
    def notify(title: str, message: str):
        # Fallback if plyer is not installed or fails
        print(f"{title}: {message}")
