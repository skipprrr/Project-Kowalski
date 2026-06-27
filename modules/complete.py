from modules.tasks import complete_latest_task
from modules.reminders import complete_latest_reminder


def process_completion(message):
    lower = message.lower()

    if (
        "done" in lower
        or "finished" in lower
        or "completed" in lower
    ):
        if complete_latest_task():
            return (
                "Excellent work, Skipper.\n\n"
                "Task marked as completed."
            )

    if (
        "paid" in lower
        or "reminded" in lower
    ):
        if complete_latest_reminder():
            return (
                "Excellent work, Skipper.\n\n"
                "Reminder marked as completed."
            )

    return None