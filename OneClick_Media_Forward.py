from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
import asyncio
import os
import time

# ============================================================
#                     CONFIGURATION
# ============================================================

api_id = XXXXXXXX
api_hash = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Files will be saved in the same folder as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
session_name = os.path.join(BASE_DIR, "forwarder_session")
log_file = os.path.join(BASE_DIR, "forwarded_ids.txt")

# Source and Target — use any of these formats:
#   '@username'        — public username
#   1234567890         — numeric ID (no quotes)
#   '+918577912442'    — phone number (with quotes)

SOURCE = XXXXXXXX   # <-- CHANGE THIS
TARGET = XXXXXXXX   # <-- CHANGE THIS

# ============================================================
#                     DO NOT EDIT BELOW
# ============================================================

def load_forwarded_ids():
    if not os.path.exists(log_file):
        return set()
    with open(log_file, 'r') as f:
        ids = set(int(line.strip()) for line in f if line.strip().isdigit())
    print(f"Loaded {len(ids)} already forwarded IDs.")
    return ids

def log_forwarded_id(msg_id):
    with open(log_file, 'a') as f:
        f.write(f"{msg_id}\n")

async def run():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()

    print("Fetching dialogs...")
    await client.get_dialogs(limit=None)

    try:
        source = await client.get_entity(SOURCE)
        print(f"Found source: {source.id}")
    except Exception as e:
        print(f"ERROR finding source: {e}")
        await client.disconnect()
        return

    try:
        target = await client.get_entity(TARGET)
        print(f"Found target: {target.id}")
    except Exception as e:
        print(f"ERROR finding target: {e}")
        await client.disconnect()
        return

    forwarded_ids = load_forwarded_ids()
    print(f"Already forwarded: {len(forwarded_ids)} messages")

    # Forward all old media messages
    async for message in client.iter_messages(source, reverse=True):
        if not message.media or message.id in forwarded_ids:
            continue
        try:
            print(f"Forwarding message ID {message.id}")
            await client.forward_messages(target, message)
            log_forwarded_id(message.id)
            forwarded_ids.add(message.id)
            await asyncio.sleep(1)  # 0.5 seconds — faster  # 0.3 seconds — even faster # 0 seconds no delay — maximum speed(very risky, Telegram will likely FloodWait you)
        except FloodWaitError as e:
            print(f"FloodWait: sleeping {e.seconds}s...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"ERROR skipping {message.id}: {e}")

    print("Done forwarding old messages. Now listening for new ones...")

    @client.on(events.NewMessage(chats=source))
    async def handler(event):
        fwd_ids = load_forwarded_ids()
        if not event.media or event.id in fwd_ids:
            return
        try:
            print(f"Live forwarding ID {event.id}")
            await client.forward_messages(target, event.message)
            log_forwarded_id(event.id)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Live ERROR: {e}")

    print("Listening for new messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(run())
        except KeyboardInterrupt:
            print("Stopped by user.")
            break
        except Exception as e:
            print(f"Crashed: {e}. Reconnecting in 10s...")
            time.sleep(10)