from datetime import datetime
from supabase import create_client
import os

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def get_or_create_user(tg_user):
    telegram_id = tg_user.id

    res = supabase.table("users_core") \
        .select("*") \
        .eq("telegram_id", telegram_id) \
        .single() \
        .execute()

    if res.data:
        supabase.table("users_core") \
            .update({"last_seen": datetime.utcnow().isoformat()}) \
            .eq("telegram_id", telegram_id) \
            .execute()
        return res.data

    user = {
        "telegram_id": telegram_id,
        "username": tg_user.username,
        "first_name": tg_user.first_name,
        "last_name": tg_user.last_name,
        "language": tg_user.language_code
    }

    created = supabase.table("users_core").insert(user).execute()
    return created.data[0]
