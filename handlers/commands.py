
from telethon import events, Button
from database import db
import asyncio

is_batch_add_link = False
is_batch_delete_link = False
batch_add_link = []
batch_delete_link = []
BATCH_SIZE = 1000

async def addlink_handler(event):
    user = db.get_user_by_telegram_id(event.sender_id)
    if not user:
        await event.respond("Please Login First To Set Settings /start", buttons=[
                    [Button.inline('Login', data='login')]
                ])
    else:
        await event.respond("Please send the sport link and type (public/private channel/group/topics), separated by a comma.\n(Example:  https://t.me/test, public)", buttons=None)
        await event.client.add_event_handler(addlink_input_handler, events.NewMessage(from_users=event.sender_id))

async def addlink_input_handler(event):
    text = event.text
    parts = text.split(",")
    if len(parts) == 2:
        url, link_type = parts
        if db.add_link(url.strip(), link_type.strip()):
           await event.respond(f"Link Successfully added {url}", buttons=[
                     [Button.inline('Settings', data='settings')]
            ])
        else:
              await event.respond(f"Link is Already added try another Link", buttons=[
                     [Button.inline('Settings', data='settings')]
            ])
    else:
        await event.respond("Invalid Input! Please send `link, type`")
    event.client.remove_event_handler(addlink_input_handler)

async def replace_link_handler(event):
    user = db.get_user_by_telegram_id(event.sender_id)
    if not user:
        await event.respond("Please Login First To Set Settings /start", buttons=[
                    [Button.inline('Login', data='login')]
                ])
    else:
          await event.respond("Please send the old link followed by the new link, separated by a comma\n(Example:  https://t.me/test1, https://t.me/test2)", buttons=None)
          await event.client.add_event_handler(replace_link_input_handler, events.NewMessage(from_users=event.sender_id))

async def replace_link_input_handler(event):
      text = event.text
      parts = text.split(",")
      if len(parts) == 2:
          old_url, new_url = parts
          db.replace_link(old_url.strip(), new_url.strip())
          await event.respond(f"Link Successfully Replace old link {old_url} to new link {new_url}", buttons=[
                        [Button.inline('Settings', data='settings')]
                    ])
      else:
          await event.respond("Invalid Input! Please send `old link, new link`")
      event.client.remove_event_handler(replace_link_input_handler)

async def show_first_last_link_handler(event, count):
    user = db.get_user_by_telegram_id(event.sender_id)
    if not user:
        await event.respond("Please Login First To Set Settings /start", buttons=[
                    [Button.inline('Login', data='login')]
                ])
    else:
      first_links = db.get_first_links(count)
      last_links = db.get_last_links(count)

      message = "First Links Not Found \n"
      if first_links:
          message = "First Links:\n"
          for index, item in enumerate(first_links):
              message += f"{index+1}. {item[1]}\n"
      else:
           message = "First Link Not Found\n"
      if last_links:
          message += "\nLast Links:\n"
          for index, item in enumerate(last_links):
             message += f"{index +1}. {item[1]}\n"
      else:
          message += "\nLast Link Not Found"
      await event.respond(message, buttons=[
                    [Button.inline('Settings', data='settings')]
                ])

async def batch_addlink_handler(event):
    global is_batch_add_link
    global batch_add_link
    user = db.get_user_by_telegram_id(event.sender_id)
    if not user:
        await event.respond("Please Login First To Set Settings /start", buttons=[
                    [Button.inline('Login', data='login')]
                ])
    else:
        is_batch_add_link = True
        batch_add_link = []
        await event.respond(f"Please send {BATCH_SIZE} sport links and type (public/private channel/group/topics), separated by a comma in each line.\n(Example:  https://t.me/test1, public)\n(https://t.me/test2, group)\nUse /cancel_batch_link to Cancel\nWhen You Are Done Send Done")
        await event.client.add_event_handler(batch_addlink_input_handler, events.NewMessage(from_users=event.sender_id))

async def batch_addlink_input_handler(event):
     global is_batch_add_link
     global batch_add_link
     if is_batch_add_link:
          text = event.text
          if text == 'Done':
              is_batch_add_link = False
              if len(batch_add_link) > BATCH_SIZE:
                  await event.respond(f"Please Send {BATCH_SIZE} Link only try again")
                  batch_add_link = []
                  return
              for item in batch_add_link:
                  url, link_type = item
                  db.add_link(url.strip(), link_type.strip())
              batch_add_link = []
              await event.respond("Batch link added Successfully", buttons=[
                        [Button.inline('Settings', data='settings')]
                    ])
              event.client.remove_event_handler(batch_addlink_input_handler)
          else:
              parts = text.split(",")
              if len(parts) == 2:
                 batch_add_link.append(parts)
              else:
                 await event.respond("Invalid Input! Please send `link, type` in Each line or send Done")

async def batch_deletelink_handler(event):
    global is_batch_delete_link
    global batch_delete_link
    user = db.get_user_by_telegram_id(event.sender_id)
    if not user:
        await event.respond("Please Login First To Set Settings /start", buttons=[
                    [Button.inline('Login', data='login')]
                ])
    else:
        is_batch_delete_link = True
        batch_delete_link = []
        await event.respond(f"Please send {BATCH_SIZE} sport links to delete\n(Example: https://t.me/test1)\n(https://t.me/test2) \nUse /cancel_batch_link to Cancel\nWhen You Are Done Send Done")
        await event.client.add_event_handler(batch_deletelink_input_handler, events.NewMessage(from_users=event.sender_id))

async def batch_deletelink_input_handler(event):
    global is_batch_delete_link
    global batch_delete_link
    if is_batch_delete_link:
          text = event.text
          if text == 'Done':
            is_batch_delete_link = False
            if len(batch_delete_link) > BATCH_SIZE:
                await event.respond(f"Please Send {BATCH_SIZE} Link only try again")
                batch_delete_link = []
                return
            for link in batch_delete_link:
                db.delete_link(link)
            batch_delete_link = []
            await event.respond("Batch link Deleted Successfully", buttons=[
                    [Button.inline('Settings', data='settings')]
                ])
            event.client.remove_event_handler(batch_deletelink_input_handler)
          else:
              batch_delete_link.append(text)

async def cancel_batch_link_handler(event):
      global is_batch_add_link
      global is_batch_delete_link
      global batch_add_link
      global batch_delete_link

      is_batch_add_link = False
      is_batch_delete_link = False
      batch_add_link = []
      batch_delete_link = []

      event.client.remove_event_handler(batch_addlink_input_handler)
      event.client.remove_event_handler(batch_deletelink_input_handler)

      await event.respond('Batch link Canceled', buttons=[
                    [Button.inline('Settings', data='settings')]
                ])
