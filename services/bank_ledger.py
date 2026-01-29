from supabase import create_client
import os
from datetime import datetime

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

def create_transaction(
    user_id,
    tx_type,
    amount,
    currency="BRL",
    reference=None,
    status="completed"
):
    data = {
        "user_id": str(user_id),
        "type": tx_type,
        "amount": amount,
        "currency": currency,
        "reference": reference,
        "status": status,
        "created_at": datetime.utcnow().isoformat()
    }

    return supabase.table("transactions").insert(data).execute().data[0]


def get_balance(user_id):
    res = (
        supabase.table("transactions")
        .select("amount")
        .eq("user_id", str(user_id))
        .eq("status", "completed")
        .execute()
    )

    return sum([float(t["amount"]) for t in res.data])
