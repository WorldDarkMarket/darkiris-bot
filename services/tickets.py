from supabase import create_client
import os

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

def create_ticket(user_id, category, service, price=None):
    res = supabase.table("tickets").insert({
        "user_id": user_id,
        "category": category,
        "service": service,
        "price": price
    }).execute()
    return res.data[0]

