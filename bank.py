from supabase import create_client
import os

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

def get_wallet(telegram_id):
    user = supabase.table("users_core") \
        .select("id") \
        .eq("telegram_id", telegram_id) \
        .single() \
        .execute().data

    wallet = supabase.table("wallets") \
        .select("*") \
        .eq("user_id", user["id"]) \
        .single() \
        .execute().data

    if wallet:
        return wallet

    created = supabase.table("wallets").insert({
        "user_id": user["id"],
        "balance": 0
    }).execute()

    return created.data[0]


def get_transactions(telegram_id):
    user = supabase.table("users_core") \
        .select("id") \
        .eq("telegram_id", telegram_id) \
        .single() \
        .execute().data

    res = supabase.table("transactions") \
        .select("*") \
        .eq("user_id", user["id"]) \
        .order("created_at", desc=True) \
        .limit(10) \
        .execute()

    return res.data


def get_bank_settings():
    return {
        "currency": "USDT",
        "deposit": ["PIX", "CRYPTO"]
    }

