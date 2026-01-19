import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_or_create_user(telegram_id, username=None):
    user = supabase.table("users").select("*").eq("telegram_id", telegram_id).execute().data
    if user:
        return user[0]
    return supabase.table("users").insert({
        "telegram_id": telegram_id,
        "username": username
    }).execute().data[0]

def load_memory(user_id, limit=10):
    data = supabase.table("darkiris_memory") \
        .select("role, content") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .limit(limit) \
        .execute().data
    return list(reversed(data)) if data else []

def save_memory(user_id, role, content):
    supabase.table("darkiris_memory").insert({
        "user_id": user_id,
        "role": role,
        "content": content
    }).execute()
