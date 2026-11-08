import os
import time
import asyncio


_last_edit = {}


def human_size(b: float) -> str:
    for u in ["B", "KB", "MB", "GB", "TB"]:
        if b < 1024:
            return f"{b:.2f} {u}"
        b /= 1024
    return f"{b:.2f} PB"


def human_time(sec: int) -> str:
    sec = int(sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m}m {s}s"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"


async def edit_status(msg, text: str, force: bool = False):
    """Telegram flood limit er jonno 4 sec throttle."""
    if msg is None:
        return
    now = time.time()
    if not force and now - _last_edit.get(msg.id, 0) < 4:
        return
    _last_edit[msg.id] = now
    try:
        await msg.edit_text(text)
    except Exception:
        pass


def cleanup(*paths):
    """Temp file gulo delete kore dey."""
    for p in paths:
        try:
            if p and os.path.exists(p):
                if os.path.isdir(p):
                    for f in os.listdir(p):
                        os.remove(os.path.join(p, f))
                    os.rmdir(p)
                else:
                    os.remove(p)
        except Exception:
            pass


class ProgressTracker:
    """Download / upload progress message er jonno."""
    def __init__(self, status_msg, prefix: str = "Downloading"):
        self.msg = status_msg
        self.prefix = prefix
        self.start = time.time()
        self.last = 0
        self.loop = None

    def _get_loop(self):
        if self.loop is None:
            try:
                self.loop = asyncio.get_running_loop()
            except RuntimeError:
                try:
                    self.loop = asyncio.get_event_loop()
                except Exception:
                    self.loop = None
        return self.loop

    def update(self, current: int, total: int):
        now = time.time()
        if now - self.last < 4:
            return
        self.last = now
        if total <= 0:
            return
        pct = current * 100 / total
        speed = current / max(now - self.start, 1)
        eta = (total - current) / max(speed, 1)
        text = (
            f"**{self.prefix}...**\n\n"
            f"`{human_size(current)} / {human_size(total)}`\n"
            f"**Progress:** `{pct:.1f}%`\n"
            f"**Speed:** `{human_size(speed)}/s`\n"
            f"**ETA:** `{human_time(eta)}`"
        )
        loop = self._get_loop()
        if loop and self.msg:
            try:
                loop.create_task(self.msg.edit_text(text))
            except Exception:
                pass
