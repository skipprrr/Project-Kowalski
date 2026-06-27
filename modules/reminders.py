from core.database import supabase


def create_reminder(
    content,
    due_text,
    category
):
    response = (
        supabase
        .table("reminders")
        .insert(
            {
                "content": content,
                "due_text": due_text,
                "category": category
            }
        )
        .execute()
    )

    return response.data


def get_reminders():
    response = (
        supabase
        .table("reminders")
        .select("*")
        .eq(
            "status",
            "pending"
        )
        .order("id")
        .execute()
    )

    return response.data


def complete_latest_reminder():
    reminders = get_reminders()

    if len(reminders) == 0:
        return False

    latest = reminders[-1]

    (
        supabase
        .table("reminders")
        .update(
            {
                "status": "completed"
            }
        )
        .eq(
            "id",
            latest["id"]
        )
        .execute()
    )

    return True
