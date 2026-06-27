from modules.complete import process_completion
from modules.memory import process_message
from ai.reply import generate_reply
from ai.brain import generate_chat_reply


def route_message(message):

    # ==========================================
    # PYTHON COMMANDS
    # ==========================================

    command = generate_reply(message)

    if command:
        return {
            "reply": command
        }

    # ==========================================
    # MEMORY / TASK / REMINDER
    # ==========================================

    save = process_message(message)

    if save["saved"]:

        if save["type"] == "task":

            return {
                "reply": "📋 Mission added."
            }

        if save["type"] == "reminder":

            due = save.get("due_text")

            if due:
                return {
                    "reply": f"⏰ Reminder saved ({due})."
                }

            return {
                "reply": "⏰ Reminder saved."
            }

        return {
            "reply": "🧠 Saved to memory."
        }

    # ==========================================
    # COMPLETION
    # ==========================================

    completion = process_completion(message)

    if completion:
        return {
            "reply": completion
        }

    # ==========================================
    # AI CHAT
    # ==========================================

    return {
        "reply": generate_chat_reply(message)
    }