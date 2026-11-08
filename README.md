# yt-m3u8-leech-bot

m3u8 link theke yt-dlp diye download kore, size onujayi split kore, Telegram e upload kore.

## Features

- `/start` → m3u8 link paste prompt
- Auto download (yt-dlp, mkv output)
- Smart split:
  - Premium session → 4GB split
  - Non-premium session → 2GB split
  - Kono session na → 50MB split (Bot API limit)
- Live status: downloading → splitting → uploading → done
- `/bsetting` → **owner only**, config dekha + instructions

## Deploy to Heroku

1. GitHub e ei repo push koro.
2. Heroku Dashboard → **New → Create new app**.
3. **Deploy** tab → GitHub connect → branch select → **Deploy Branch**.
4. **Settings → Buildpacks** — duita add koro ei order e:
   - `https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest`
   - `heroku/python`
5. **Settings → Config Vars** — niche list onujayi add koro.
6. **Resources** tab → **worker** dyno on koro (`standard-2x` recommend).
7. Bot PM e `/start` diye test koro.

## Required Config Vars

| Key | Value |
|---|---|
| BOT_TOKEN | @BotFather token |
| API_ID | my.telegram.org |
| API_HASH | my.telegram.org |
| OWNER_ID | tomar user id (@userinfobot theke) |
| USER_SESSION_STRING | optional (non-premium, 2GB) |
| PREMIUM_SESSION_STRING | optional (premium, 4GB) |
| TG_SPLIT_SIZE | 2147483648 (2GB) |
| PREMIUM_SPLIT_SIZE | 4294967296 (4GB) |
| FRAGMENT_WORKERS | 16 (32 risky) |
| UPLOAD_CHAT_ID | me |

## Session String kibhabe banabo

Pyrogram v2 session generator use koro:
- https://replit.com/@ayrahikari/pyrogram-session-maker

- Non-premium account → `USER_SESSION_STRING`
- Premium account → `PREMIUM_SESSION_STRING`

## Notes

- Heroku te `/tmp` ephemeral, tai file upload sesh e delete hoy.
- Bot API 50MB limit — boro file er jonno user session lagbe.
- `FRAGMENT_WORKERS=32` dile onek server rate-limit dey, 8-16 safe.
- Boro file (3GB+) er jonno `standard-2x` dyno lagbe.
- `/bsetting` command **shudhu OWNER_ID** use korte parbe.
