from supabase import create_client
import os
from datetime import datetime

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

def create_ticket(
    user_id,
    store_slug,
    service_code,
    title,
    price,
    description=None,
    payment_required=False,
    ticket_required=True
):
    data = {
        "user_id": str(user_id),
        "store_slug": store_slug,
        "service_code": service_code,
        "title": title,
        "price": price,
        "payment_required": payment_required,
        "ticket_required": ticket_required,
        "status": "waiting_payment" if payment_required else "open",
        "created_at": datetime.utcnow().isoformat()
    }

    res = supabase.table("tickets_core").insert(data).execute()
    return res.data[0]


def mark_ticket_paid(ticket_id):
    supabase.table("tickets_core") \
        .update({"status": "paid"}) \
        .eq("id", ticket_id) \
        .execute()


