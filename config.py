    import os
    from dotenv import load_dotenv

    load_dotenv()

    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    MONGODB_URL = os.getenv("MONGODB_URL")
    REACTION_EMOJI = os.getenv("REACTION_EMOJI", "👍")

    # Load Admin Ids from .env or empty list
    ADMIN_IDS = [int(admin_id) for admin_id in os.getenv("ADMIN_IDS", "").split(",") if admin_id] or []
    # Load Log channel id from .env if it exist
    LOG_CHANNEL = os.getenv("LOG_CHANNEL")
    if LOG_CHANNEL:
        LOG_CHANNEL = int(LOG_CHANNEL) # convert to integer
    else:
       LOG_CHANNEL = None #Set None if the LOG_CHANNEL variable is missing
