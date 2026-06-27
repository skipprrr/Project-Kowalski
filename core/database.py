from supabase import create_client
from core.config import (
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY,
)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY
)


def save_memory(
    content,
    category,
    tags
):
    response = (
        supabase
        .table("memories")
        .insert(
            {
                "content": content,
                "category": category,
                "tags": tags,
            }
        )
        .execute()
    )

    return response.data