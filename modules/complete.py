import re

from modules.tasks import complete_latest_task
from modules.reminders import complete_latest_reminder


TASK_COMPLETION_PATTERNS = [
    r"^done$",
    r"^done\s+(with\s+)?(it|task|mission|this)$",
    r"^task\s+done$",
    r"^mission\s+done$",
    r"^mark\s+(the\s+)?(task|mission)\s+(as\s+)?done$",
    r"^finished$",
    r"^finished\s+(it|the\s+task|the\s+mission|task|mission)$",
    r"^completed$",
    r"^completed\s+(it|the\s+task|the\s+mission|task|mission)$",
    r"^i\s+(am|'m)\s+done$",
    r"^i\s+finished(\s+it)?$",
    r"^i\s+completed\s+it$",
]

REMINDER_COMPLETION_PATTERNS = [
    r"^paid$",
    r"^paid\s+.+$",
    r"^i\s+paid(\s+.+)?$",
    r"^payment\s+paid$",
    r"^reminded$",
    r"^reminder\s+done$",
    r"^mark\s+(the\s+)?reminder\s+(as\s+)?done$",
]


def matches_any(patterns, message):
    return any(
        re.match(pattern, message)
        for pattern in patterns
    )


def process_completion(message):
    lower = message.lower().strip()

    if matches_any(TASK_COMPLETION_PATTERNS, lower):
        if complete_latest_task():
            return (
                "Excellent work, Skipper.\n\n"
                "Task marked as completed."
            )

    if matches_any(REMINDER_COMPLETION_PATTERNS, lower):
        if complete_latest_reminder():
            return (
                "Excellent work, Skipper.\n\n"
                "Reminder marked as completed."
            )

    return None
