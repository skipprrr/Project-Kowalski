from core.database import supabase


def search_memories(query):
    response = (
        supabase
        .table("memories")
        .select("*")
        .ilike("content", f"%{query}%")
        .execute()
    )

    return response.data