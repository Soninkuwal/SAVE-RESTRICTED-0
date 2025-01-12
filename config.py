    import os
    from dotenv import load_dotenv

    load_dotenv()

    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    MONGODB_URL = os.getenv("MONGODB_URL")
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))
    REACTION_EMOJI = os.getenv("REACTION_EMOJI", "👍")
    ADMIN_IDS = [int(admin_id) for admin_id in os.getenv("ADMIN_IDS", "").split(",") if admin_id]
