from features.today import generate_today
from features.money import money_command

from modules.tasks import get_tasks
from modules.reminders import get_reminders
from modules.search import search_memories


def generate_reply(message):

    lower = message.lower().strip()

    # ==========================================
    # MONEY
    # ==========================================

    money = money_command(message)

    if money:
        return money

    # ==========================================
    # TODAY
    # ==========================================

    if lower in [
        "today",
        "/today"
    ]:
        return generate_today()

    # ==========================================
    # TASKS
    # ==========================================

    if lower in [
        "task",
        "tasks",
        "mission",
        "missions",
        "show my tasks"
    ]:

        tasks = get_tasks()

        if not tasks:
            return "📋 No active missions."

        response = "📋 Current Missions\n\n"

        for task in tasks:
            response += f"• {task['content']}\n"

        return response

    # ==========================================
    # REMINDERS
    # ==========================================

    if lower in [
        "reminder",
        "reminders",
        "show reminders",
        "my reminders"
    ]:

        reminders = get_reminders()

        if not reminders:
            return "⏰ No pending reminders."

        response = "⏰ Current Reminders\n\n"

        for reminder in reminders:

            response += f"• {reminder['content']}"

            if reminder["due_text"]:
                response += f" ({reminder['due_text']})"

            response += "\n"

        return response

    # ==========================================
    # SEARCH
    # ==========================================

    if (
        lower.startswith("search ")
        or lower.startswith("find ")
        or lower.startswith("show ")
        or lower.startswith("what do you remember")
    ):

        results = search_memories(message)

        if not results:
            return "Nothing found."

        response = "🧠 Archive\n\n"

        for item in results:
            response += f"• {item['content']}\n"

        return response

    return None