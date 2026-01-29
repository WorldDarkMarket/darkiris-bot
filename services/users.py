from datetime import datetime
from services.supabase_client import supabase

def get_or_create_user(tg_user):
    telegram_id = tg_user.id

    res = (
        supabase.table("users_core")
        .select("*")
        .eq("telegram_id", telegram_id)
        .limit(1)
        .execute()
    )

    if res.data and len(res.data) > 0:
        supabase.table("users_core") \
            .update({"last_seen": datetime.utcnow().isoformat()}) \
            .eq("telegram_id", telegram_id) \
            .execute()
        return res.data[0]

    user = {
        "telegram_id": telegram_id,
        "username": tg_user.username,
        "first_name": tg_user.first_name,
        "last_name": tg_user.last_name,
        "language": tg_user.language_code
    }

    created = supabase.table("users_core").insert(user).execute()
    return created.data[0]



