from core.database import supabase


SEARCH_PREFIXES = [
    "what do you remember about",
    "what do you remember",
    "search",
    "find",
    "show",
]


def parse_search_query(query):
    cleaned = query.strip()
    lower = cleaned.lower()

    for prefix in SEARCH_PREFIXES:
        if lower == prefix:
            return ""

        prefix_with_space = f"{prefix} "

        if lower.startswith(prefix_with_space):
            return cleaned[len(prefix_with_space):].strip()

    return cleaned


def search_memories(query):
    search_text = parse_search_query(query)

    if not search_text:
        return []

    response = (
        supabase
        .table("memories")
        .select("*")
        .ilike("content", f"%{search_text}%")
        .execute()
    )

    return response.data
