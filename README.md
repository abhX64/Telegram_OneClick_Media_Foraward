# OneClick Media Forwarder 

A Python script that automatically forwards all media messages (photos, videos, files) from any Telegram source (group, channel, DM, username) to any target — including real-time live forwarding.

---

## Features

- Forwards all old media messages from source to target
- Listens and forwards new media messages in real-time
- Skips already forwarded messages (no duplicates)
- Auto-resumes after restart from where it left off
- Handles Telegram FloodWait automatically
- Auto-reconnects on network drop or crash
- Works with groups, channels, DMs, and public usernames

---

## Requirements

- Windows / Mac / Linux
- Python 3.7 or higher (recommended: 3.11)
- A Telegram account
- Telegram API credentials (free)

---

## Step 1 — Install Python

1. Go to https://www.python.org/downloads/
2. Download and install Python 3.11 (recommended)
3. During installation, **make sure to check "Add Python to PATH"**
4. Open Command Prompt and verify:
   ```
   python --version
   ```
   You should see something like `Python 3.11.x`

---

## Step 2 — Install Required Library

Open Command Prompt and run:

```
pip install telethon
```

---

## Step 3 — Get Telegram API Credentials

You need a free API ID and API Hash from Telegram.

1. Go to https://my.telegram.org
2. Log in with your Telegram phone number
3. Click **"API Development Tools"**
4. Fill in any app name (e.g. `MyForwarder`) and platform (e.g. `Desktop`)
5. Click **Create Application**
6. You will see your **`api_id`** (a number) and **`api_hash`** (a long string)
7. Copy both — you'll need them in the script

---

## Step 4 — Configure the Script

Open `OneClick_Media_Forward_V2.py` in any text editor (Notepad, VS Code, etc.)

Find this section at the top:

```python
api_id = XXXXXXXX                              # <-- Replace with your api_id
api_hash = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # <-- Replace with your api_hash

SOURCE = '@username_here'   # <-- Where to forward FROM
TARGET = '@username_here'   # <-- Where to forward TO
```

### Setting SOURCE and TARGET

You can use any of these formats:

| Format | Example | Works For |
|--------|---------|-----------|
| `'@username'` | `'@mychannel'` | Public channels, groups, users |
| Numeric ID | `1234567890` | Any chat you are a member of |
| Phone number | `'+91XXXXXXXXXX'` | Contacts saved in your Telegram |

#### Examples:

```python
# Forward from a public channel to your group
SOURCE = '@bigchannel'
TARGET = '@mygroup'

# Forward from a group (numeric ID) to another group
SOURCE = 381XXXXXXX
TARGET = XXXXXXX263

# Mix both formats
SOURCE = '@bigchannel'
TARGET = 515XXXXXXX
```

### How to find Numeric ID of a group/channel

**Option 1 — From Telegram Web:**
1. Open https://web.telegram.org
2. Click on the group or channel
3. Look at the URL — e.g. `web.telegram.org/k/#-100XXXXXXX890`
4. The number after `#-100` is the ID → `1234567890`

**Option 2 — Run the script once:**
If the script can't find your source/target, it will automatically print a list of all your chats with their IDs. Copy the correct ID from that list.

---

## Step 5 — Run the Script

1. Open Command Prompt
2. Navigate to the folder where the script is saved:
   ```
   cd "C:\Users\YourName\Downloads"
   ```
3. Run the script:
   ```
   python OneClick_Media_Forward.py
   ```
4. First time only — it will ask for:
   - Your phone number (with country code, e.g. `+91XXXXXXXXXX`)
   - The OTP code sent to your Telegram app
5. After login, it will start forwarding automatically

---

## Step 6 — What Happens When You Run It

```
Fetching dialogs...
Found source: 1234567890
Found target: 9876543210
Loaded 0 already forwarded IDs.
Already forwarded: 0 messages
Forwarding message ID 1
Forwarding message ID 2
Forwarding message ID 3
...
Done forwarding old messages. Now listening for new ones...
Listening for new messages...
```

- It first forwards all old media from the source
- Then it stays running and forwards any new media in real-time
- Press `Ctrl + C` to stop

---

## Files Created by the Script

| File | Purpose |
|------|---------|
| `forwarder_session.session` | Saves your Telegram login (so it doesn't ask every time) |
| `forwarded_ids.txt` | Saves IDs of forwarded messages (prevents duplicates) |

Both files are created automatically in the same folder as the script.

> **Note:** If you want to start fresh and re-forward everything, delete `forwarded_ids.txt`. If you want to re-login, delete `forwarder_session.session`.

---

## Adjusting Forward Speed

In the script, find this line:

```python
await asyncio.sleep(1)
```

Change the number to control speed:

| Value | Speed | Risk |
|-------|-------|------|
| `1` | Safe, 1 message/sec | No risk |
| `0.5` | Faster | Low risk |
| `0.3` | Fast | Medium risk |
| `0` | Maximum speed | High risk of FloodWait |

> Telegram may temporarily ban forwarding if you go too fast. The script handles this automatically and resumes after the wait.

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Could not find source` | You are not a member of the source group/channel | Join the group/channel first |
| `FloodWait` | Forwarding too fast | Script handles this automatically |
| `WinError 1236` | Network dropped | Script reconnects automatically |
| `Session error` | Corrupted session file | Delete `forwarder_session.session` and re-run |
| `api_id invalid` | Wrong API credentials | Double-check your api_id and api_hash |
| `ChatForwardsRestrictedError` | Source has restricted forwarding | Cannot bypass — Telegram restriction |

---

## Important Notes

- You must be a **member** of both the source and target group/channel
- This script uses your **personal Telegram account** — use responsibly
- Forwarding too aggressively may get your account flagged by Telegram
- Do **not** share your `api_hash` or `forwarder_session.session` with anyone

---

## .gitignore

Create a `.gitignore` file in your repo to avoid accidentally uploading sensitive files:

```
forwarder_session.session
forwarded_ids.txt
__pycache__/
*.pyc
```

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 abhX64

---

## Disclaimer

This tool is for **educational purposes only**. The author is not responsible for any misuse. Use in compliance with [Telegram's Terms of Service](https://telegram.org/tos).
