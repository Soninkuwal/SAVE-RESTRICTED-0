# SAVE-RESTRICTED-0

    # Telegram Sports Bot

    This bot is designed to manage and share sports-related links from Telegram channels, groups, and topics.

    ## Features

    *   **Link Management:**
        *   Store links from public/private channels, groups, and topic groups.
        *   Add, delete links with custom type
        *   Batch import links from text file.
    *   **Welcome Message:**
        *   Send a welcome message with an image and "Join" buttons for multiple saved links.
    *   **User Authentication:**
        *   Login with phone number and country code.
        *   Logout.
    *   **Settings:**
        *   Upload custom thumbnail.
        *   Replace custom words in links.
        *   Delete custom words in links.
        *    Cancel batch import
        *   Broadcast Message to all users
    *   **Auto Reaction Emoji:**
        *   Bot auto-reacts to all user commands with a specified emoji.
    *   **User Logging:**
        *   Log new users, user IDs, and profile details to a log channel.

    ## Commands

    *   `/start`: Start the bot and see the welcome message with join links.
    *   `/help`: Get a list of available bot commands.
    *   `/login`: Login to the bot using phone number with country code.
    *   `/logout`: Logout from bot.
    *   `/settings`: Open the bot settings menu.
    *   `/add_link <type> <link>`: Add a link with specified type (public, private, or topic)
    *   `/delete_link <link_id>`: Delete a specific link.
    *    `/broadcast <message>`: Send broadcast message to all bot users.

    ## Setup

    1.  **Install Python:** Ensure you have Python 3.7+ installed.
    2.  **Install dependencies:**
