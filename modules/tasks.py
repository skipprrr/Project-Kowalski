from core.database import supabase


def create_task(content):
    response = (
        supabase
        .table("tasks")
        .insert(
            {
                "content": content
            }
        )
        .execute()
    )

    return response.data


def get_tasks():
    response = (
        supabase
        .table("tasks")
        .select("*")
        .eq("status", "active")
        .execute()
    )

    return response.data


def complete_latest_task():
    tasks = get_tasks()

    if len(tasks) == 0:
        return False

    latest_task = tasks[-1]

    (
        supabase
        .table("tasks")
        .update(
            {
                "status": "completed"
            }
        )
        .eq(
            "id",
            latest_task["id"]
        )
        .execute()
    )

    return True