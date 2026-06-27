from core.database import save_memory
from modules.tasks import create_task
from modules.reminders import create_reminder


REMINDER_PREFIXES = [
    "remind me ",
    "remind ",
]

MEMORY_PREFIXES = [
    "remember",
    "note",
    "save",
]


def parse_reminder_due(message):
    lower = message.lower().strip()

    if lower in ["remind", "remind me"]:
        return None

    reminder_text = None

    for prefix in REMINDER_PREFIXES:
        if lower.startswith(prefix):
            reminder_text = lower[len(prefix):].strip()
            break

    if reminder_text is None:
        return None

    if reminder_text.startswith("tomorrow"):
        return "tomorrow"

    if reminder_text.startswith("today"):
        return "today"

    if reminder_text.startswith("tonight"):
        return "tonight"

    if reminder_text.startswith("at "):
        time_text = reminder_text[3:].split()[0].strip(".,")

        if time_text:
            return f"at {time_text}"

    if "tomorrow" in lower:
        return "tomorrow"

    if "today" in lower:
        return "today"

    return None


def is_reminder(message):
    lower = message.lower().strip()

    if lower in ["remind", "remind me"]:
        return True

    return any(
        lower.startswith(prefix)
        for prefix in REMINDER_PREFIXES
    )


def is_memory_note(message):
    lower = message.lower().strip()

    return any(
        lower == prefix or lower.startswith(f"{prefix} ")
        for prefix in MEMORY_PREFIXES
    )


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

    if is_reminder(message):

        due_text = parse_reminder_due(message)

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

    if is_memory_note(message):

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
