from core.database import save_memory
from modules.tasks import create_task
from modules.reminders import create_reminder


def process_message(message):

    lower = message.lower().strip()

    # -----------------------------
    # TASK
    # -----------------------------

    if (
        lower.startswith("i need to")
        or lower.startswith("todo")
    ):

        create_task(message)

        return {
            "saved": True,
            "type": "task"
        }

    # -----------------------------
    # REMINDER
    # -----------------------------

    if lower.startswith("remind me"):

        due_text = None

        if "tomorrow" in lower:
            due_text = "tomorrow"

        elif "today" in lower:
            due_text = "today"

        create_reminder(
            message,
            due_text,
            "Reminders"
        )

        save_memory(
            message,
            "Reminders",
            ["Reminder"]
        )

        return {
            "saved": True,
            "type": "reminder",
            "due_text": due_text
        }

    # -----------------------------
    # NOTE
    # -----------------------------

    if (
        lower.startswith("remember")
        or lower.startswith("note")
        or lower.startswith("save")
    ):

        save_memory(
            message,
            "General",
            []
        )

        return {
            "saved": True,
            "type": "note",
            "category": "General"
        }

    # -----------------------------
    # NOTHING TO SAVE
    # -----------------------------

    return {
        "saved": False
    }