import os
import yt_dlp
from config import DOWNLOAD_DIR, FRAGMENT_WORKERS
from helpers import ProgressTracker


def download_m3u8(url: str, status_msg=None) -> str:
    """
    m3u8 link theke download kore mkv file return kore.
    Progress status_msg e update hoy.
    """
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    tracker = ProgressTracker(status_msg, "File is downloading") if status_msg else None

    def hook(d):
        if d.get("status") == "downloading" and tracker:
            tracker.update(
                d.get("downloaded_bytes", 0),
                d.get("total_bytes") or d.get("total_bytes_estimate", 0),
            )

    ydl_opts = {
        "format": "bv*+ba/b",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "merge_output_format": "mkv",                       # mkv te upload
        "concurrent_fragment_downloads": FRAGMENT_WORKERS,  # -N
        "quiet": True,
        "noprogress": True,
        "no_warnings": True,
        "progress_hooks": [hook],
        "retries": 5,
        "fragment_retries": 10,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        path = ydl.prepare_filename(info)

    # prepare_filename ext mkv na-o hote pare, tai actual file khuje ber kori
    if not os.path.exists(path):
        base = os.path.splitext(path)[0]
        for ext in (".mkv", ".mp4", ".webm"):
            if os.path.exists(base + ext):
                return base + ext
    return path
