from modules.money import (
    add_money,
    clear_money,
    get_pending,
    get_person,
    get_summary,
    normalize_person_name,
)


ADD_EXAMPLE = "Example:\n\nmoney add Fatima | 2500 | Reel Edit"


def format_amount(amount):
    return f"Tk {int(amount)}"


def money_command(message):

    lower = message.strip().lower()

    if lower != "money" and not lower.startswith("money "):
        return None

    command = message[5:].strip()
    command_lower = command.lower()

    try:

        # ==========================================
        # MONEY
        # ==========================================

        if command == "":

            summary = get_summary()

            response = "Money Dashboard\n\n"

            response += f"Pending: {format_amount(summary['total'])}\n\n"

            if len(summary["people"]) == 0:

                response += "Nobody owes you money."

            else:

                response += "People:\n"

                for person, amount in summary["people"].items():

                    response += f"- {person} - {format_amount(amount)}\n"

            return response

        # ==========================================
        # MONEY ADD
        # ==========================================

        if command_lower.startswith("add"):

            data = command[3:].strip()

            parts = [
                x.strip()
                for x in data.split("|")
            ]

            if len(parts) != 3:
                return ADD_EXAMPLE

            person, amount_text, note = parts

            person = normalize_person_name(person)

            if not person:
                return "Who owes you money?\n\n" + ADD_EXAMPLE

            try:
                amount = int(amount_text)
            except ValueError:
                return "Amount must be a whole number.\n\n" + ADD_EXAMPLE

            if amount <= 0:
                return "Amount must be greater than 0.\n\n" + ADD_EXAMPLE

            add_money(
                person,
                amount,
                note
            )

            return (
                "Money added.\n\n"
                f"{person} owes you {format_amount(amount)}."
            )

        # ==========================================
        # MONEY PENDING
        # ==========================================

        if command_lower == "pending":

            pending = get_pending()

            if len(pending) == 0:
                return "Nobody owes you money."

            response = "Pending Money\n\n"

            total = 0

            for item in pending:

                person = normalize_person_name(item["person"])
                amount = int(item["amount"])
                note = item.get("note")

                total += amount

                response += (
                    f"- {person} - "
                    f"{format_amount(amount)}"
                )

                if note:
                    response += f" ({note})"

                response += "\n"

            response += f"\nTotal: {format_amount(total)}"

            return response

        # ==========================================
        # MONEY CLEAR
        # ==========================================

        if command_lower.startswith("clear"):

            person = normalize_person_name(command[5:].strip())

            if not person:
                return "Who should I clear?\n\nExample:\n\nmoney clear Fatima"

            cleared = clear_money(person)

            if cleared == 0:
                return f"No pending money found for {person}."

            entry_word = "entry" if cleared == 1 else "entries"

            return f"Cleared {cleared} pending money {entry_word} for {person}."

        # ==========================================
        # MONEY PERSON
        # ==========================================

        person = normalize_person_name(command)

        if not person:
            return "Try: money, money pending, or money add Fatima | 2500 | Reel Edit"

        history = get_person(person)

        if len(history) == 0:

            return f"Nothing found for {person}."

        response = f"{person}\n\n"

        earned = 0
        pending = 0

        for item in history:

            amount = int(item["amount"])
            status = item["status"]
            note = item.get("note")

            earned += amount

            if status.lower() == "pending":
                pending += amount

            response += (
                f"- {format_amount(amount)} "
                f"[{status}]"
            )

            if note:
                response += f" - {note}"

            response += "\n"

        response += (
            f"\nTotal: {format_amount(earned)}"
            f"\nPending: {format_amount(pending)}"
        )

        return response

    except Exception as e:

        print("\n========== MONEY ERROR ==========")
        print(type(e).__name__)
        print(e)
        print("=================================\n")

        return "Something went wrong with Money. Please try again."
