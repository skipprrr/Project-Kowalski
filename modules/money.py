from core.database import supabase


# ==========================================
# ADD
# ==========================================

def add_money(person, amount, note=""):

    supabase.table("money").insert({

        "person": person,
        "amount": amount,
        "note": note,
        "status": "Pending"

    }).execute()


# ==========================================
# CLEAR
# ==========================================

def clear_money(person):

    supabase.table("money") \
        .update({
            "status": "Paid"
        }) \
        .eq("person", person) \
        .eq("status", "Pending") \
        .execute()


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


# ==========================================
# PERSON
# ==========================================

def get_person(person):

    response = (
        supabase
        .table("money")
        .select("*")
        .eq("person", person)
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

        person = item["person"]

        amount = int(item["amount"])

        total += amount

        if person not in people:
            people[person] = 0

        people[person] += amount

    return {

        "people": people,

        "total": total

    }