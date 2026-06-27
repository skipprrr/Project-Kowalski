from core.database import supabase


def normalize_person_name(person):
    cleaned = " ".join(str(person or "").strip().split())

    if not cleaned:
        return ""

    return cleaned.title()


# ==========================================
# ADD
# ==========================================

def add_money(person, amount, note=""):

    normalized_person = normalize_person_name(person)

    response = supabase.table("money").insert({

        "person": normalized_person,
        "amount": amount,
        "note": note.strip(),
        "status": "Pending"

    }).execute()

    return response.data


# ==========================================
# CLEAR
# ==========================================

def clear_money(person):

    normalized_person = normalize_person_name(person)

    pending = get_person_pending(normalized_person)

    if len(pending) == 0:
        return 0

    supabase.table("money") \
        .update({
            "status": "Paid",
            "person": normalized_person
        }) \
        .ilike("person", normalized_person) \
        .eq("status", "Pending") \
        .execute()

    return len(pending)


# ==========================================
# PENDING
# ==========================================

def get_pending():

    response = (
        supabase
        .table("money")
        .select("*")
        .eq("status", "Pending")
        .order("created_at")
        .execute()
    )

    return response.data


def get_person_pending(person):

    normalized_person = normalize_person_name(person)

    response = (
        supabase
        .table("money")
        .select("*")
        .ilike("person", normalized_person)
        .eq("status", "Pending")
        .order("created_at")
        .execute()
    )

    return response.data


# ==========================================
# PERSON
# ==========================================

def get_person(person):

    normalized_person = normalize_person_name(person)

    response = (
        supabase
        .table("money")
        .select("*")
        .ilike("person", normalized_person)
        .order("created_at")
        .execute()
    )

    return response.data


# ==========================================
# TOTAL PENDING
# ==========================================

def get_total_pending():

    total = 0

    for item in get_pending():

        total += int(item["amount"])

    return total


# ==========================================
# SUMMARY
# ==========================================

def get_summary():

    pending = get_pending()

    people = {}

    total = 0

    for item in pending:

        person = normalize_person_name(item["person"])

        amount = int(item["amount"])

        total += amount

        if person not in people:
            people[person] = 0

        people[person] += amount

    return {

        "people": people,

        "total": total

    }
