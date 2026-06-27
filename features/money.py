from modules.money import (
    add_money,
    clear_money,
    get_pending,
    get_person,
    get_summary,
)


def money_command(message):

    lower = message.strip().lower()

    if not lower.startswith("money"):
        return None

    command = message[5:].strip()

    # ==========================================
    # MONEY
    # ==========================================

    if command == "":

        summary = get_summary()

        response = "💰 Money Dashboard\n\n"

        response += f"Pending: ৳{summary['total']}\n\n"

        if len(summary["people"]) == 0:

            response += "Nobody owes you money."

        else:

            response += "People:\n"

            for person, amount in summary["people"].items():

                response += f"• {person} - ৳{amount}\n"

        return response

    # ==========================================
    # MONEY ADD
    # ==========================================

    if command.startswith("add"):

        try:

            data = command[3:].strip()

            person, amount, note = [
                x.strip()
                for x in data.split("|")
            ]

            add_money(
                person,
                int(amount),
                note
            )

            return (
                "💰 Added Successfully\n\n"
                f"{person} owes you ৳{amount}"
            )

        except:

            return (
                "Example:\n\n"
                "money add Fatima | 2500 | Reel Edit"
            )

    # ==========================================
    # MONEY PENDING
    # ==========================================

    if command == "pending":

        pending = get_pending()

        if len(pending) == 0:
            return "Nobody owes you money."

        response = "💰 Pending Money\n\n"

        total = 0

        for item in pending:

            amount = int(item["amount"])

            total += amount

            response += (
                f"• {item['person']} - "
                f"৳{amount}"
            )

            if item["note"]:
                response += f" ({item['note']})"

            response += "\n"

        response += f"\nTotal: ৳{total}"

        return response

    # ==========================================
    # MONEY CLEAR
    # ==========================================

    if command.startswith("clear"):

        person = command[5:].strip()

        clear_money(person)

        return f"✅ Cleared pending money for {person}."

    # ==========================================
    # MONEY PERSON
    # ==========================================

    history = get_person(command)

    if len(history) == 0:

        return "Nothing found."

    response = f"👤 {command}\n\n"

    earned = 0
    pending = 0

    for item in history:

        amount = int(item["amount"])

        earned += amount

        if item["status"] == "Pending":
            pending += amount

        response += (
            f"• ৳{amount} "
            f"[{item['status']}]"
        )

        if item["note"]:
            response += f" - {item['note']}"

        response += "\n"

    response += (
        f"\nTotal: ৳{earned}"
        f"\nPending: ৳{pending}"
    )

    return response