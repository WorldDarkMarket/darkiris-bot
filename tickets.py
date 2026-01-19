from supabase import create_client
import os

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

def create_ticket(user_id, product_id):
    return supabase.table("tickets").insert({
        "user_id": user_id,
        "product_id": product_id,
        "status": "open"
    }).execute()
