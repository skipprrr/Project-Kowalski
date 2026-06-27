from modules.tasks import get_tasks
from modules.reminders import get_reminders


def generate_today():

    tasks = get_tasks()
    reminders = get_reminders()

    response = "📅 Good day, Skipper.\n\n"

    # ===============================
    # MISSIONS
    # ===============================

    response += "📋 Today's Missions\n"

    if not tasks:
        response += "• Nothing pending.\n"
    else:
        for task in tasks:
            response += f"• {task['content']}\n"

    response += "\n"

    # ===============================
    # REMINDERS
    # ===============================

    response += "⏰ Today's Reminders\n"

    if not reminders:
        response += "• None.\n"
    else:
        for reminder in reminders:
            due = reminder.get("due_text")

            if due:
                response += f"• {reminder['content']} ({due})\n"
            else:
                response += f"• {reminder['content']}\n"

    response += "\n"

    # ===============================
    # FOCUS
    # ===============================

    response += "🎯 Suggested Focus\n"

    if tasks:
        response += f"Start with:\n• {tasks[0]['content']}"
    else:
        response += "You're all caught up."

    return response