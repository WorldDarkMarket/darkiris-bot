from supabase import create_client
import os

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

def get_user_role(telegram_id):
    res = supabase.table("users").select("role").eq("telegram_id", telegram_id).execute()
    return res.data[0]["role"] if res.data else "user"

def is_super_admin(telegram_id):
    return get_user_role(telegram_id) == "super_admin"

def is_admin_for_store(user_id, store_id):
    res = supabase.table("admin_access") \
        .select("*") \
        .eq("user_id", user_id) \
        .eq("store_id", store_id) \
        .execute()
    return bool(res.data)
