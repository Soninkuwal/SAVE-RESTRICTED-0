# SAVE-RESTRICTED-0

# Telegram Sport Link Bot

This Telegram bot allows you to manage restricted sport links for public and private channels, groups, and topic groups. It also provides user authentication, settings customization, and broadcast functionality.

## Features

•   **Link Management:**
    •   Store sport links.
    •   Add, delete, and replace individual links.
    •   Batch add/delete 1000 links at a time.
    •   Cancel an ongoing batch operation.
•   **User Authentication:**
    •   Login using a phone number with country code.
    •   Logout using a phone number.
•   **Settings:**
    •   Set a custom thumbnail for sports content.
    •   Add custom words to replace in messages.
    •   Add custom words to delete from messages.
•   **Broadcasting:**
    •   Send broadcast messages to all logged-in users.
•   **Logging:**
    •   Log new user details (ID, profile) to a designated log channel.

## Bot Commands

```
start - Start the bot and show login button
login - Start the login process
logout - Log out of the bot
settings - Open the settings menu
addlink - Add a new link
replace_link - Replace an old link with new link
show_first_last_number - Show first and last links
batch_addlink - Start batch addition of links
batch_deletelink - Start batch deletion of links
cancel_batch_link - cancel ongoing batch operation
broadcast - Send a broadcast message
```

## Settings Menu

•   **Custom Thumbnail:** Set a URL for a custom thumbnail.
•   **Add Replace Word:** Add a word and its replacement.
•   **Add Delete Word:** Add a word to be removed from messages.

## How to Use

1.  Send `/start` to the bot to start.
2.  Login using your phone number with country code.
3.  Use `/settings` to customize thumbnails, words to replace or delete.
4.  Use other commands to manage your sport links and send broadcasts.
5.  Use `/logout` to logout.

## Deployment

1.  Build a Docker Image: `docker build -t telegram_sport_bot .`
2.  Deploy the bot to your server (Koyeb or Render). Make sure to set the port to 8080 and environment variables.

## Environment Variables

•   `API_ID`: Your Telegram API ID.
•   `API_HASH`: Your Telegram API Hash.
•   `BOT_TOKEN`: Your Telegram Bot Token.
•   `DATABASE_URL`: URL for the SQLite database.
•   `LOG_CHANNEL_ID`: ID of the channel where new user logs should be sent.
