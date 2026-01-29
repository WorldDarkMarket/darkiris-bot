from supabase import create_client
import os

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

def add_transaction(user_id, amount, tx_type, description=None, ticket_id=None):
    tx = {
        "user_id": user_id,
        "amount": amount,
        "type": tx_type,
        "description": description,
        "ticket_id": ticket_id
    }

    supabase.table("transactions_core").insert(tx).execute()
    recalc_wallet(user_id)

def recalc_wallet(user_id):
    res = supabase.table("transactions_core") \
        .select("amount") \
        .eq("user_id", user_id) \
        .execute()

    balance = sum(float(t["amount"]) for t in res.data)

    supabase.table("wallets_core").upsert({
        "user_id": user_id,
        "balance": balance
    }).execute()

    return balance
