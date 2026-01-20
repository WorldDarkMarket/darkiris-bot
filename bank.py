from supabase import Client

def get_wallet(supabase: Client, user_id: str):
    res = supabase.table("wallets").select("*").eq("user_id", user_id).execute()
    if res.data:
        return res.data[0]

    wallet = {
        "user_id": user_id,
        "balance_brl": 0,
        "balance_usdt": 0,
        "balance_ton": 0
    }
    supabase.table("wallets").insert(wallet).execute()
    return wallet

def get_bank_settings(supabase: Client):
    res = supabase.table("bank_settings").select("*").eq("id", 1).execute()
    return res.data[0]

def get_transactions(supabase: Client, user_id: str, limit=10):
    res = (
        supabase.table("transactions")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return res.data or []
