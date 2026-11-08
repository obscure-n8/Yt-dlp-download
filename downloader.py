import os
import shutil
import yt_dlp
import imageio_ffmpeg
from config import DOWNLOAD_DIR, FRAGMENT_WORKERS
from helpers import ProgressTracker


def _get_ffmpeg_path() -> str:
    """
    imageio-ffmpeg theke bundled ffmpeg er path ber kore.
    Eta na thakle system ffmpeg try kore.
    """
    try:
        path = imageio_ffmpeg.get_ffmpeg_exe()
        if path and os.path.exists(path):
            return path
    except Exception:
        pass

    # fallback: system ffmpeg
    sys_ffmpeg = shutil.which("ffmpeg")
    if sys_ffmpeg:
        return sys_ffmpeg

    raise RuntimeError(
        "ffmpeg paoa jacche na. requirements.txt e 'imageio-ffmpeg' ache kina check koro."
    )


def download_m3u8(url: str, status_msg=None) -> str:
    """
    m3u8 link theke download kore mkv file return kore.
    - imageio-ffmpeg er bundled ffmpeg use kore
    - progress status_msg e update hoy
    - final file mkv te merge hoy
    """
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    ffmpeg_path = _get_ffmpeg_path()
    ffmpeg_dir = os.path.dirname(ffmpeg_path)

    tracker = ProgressTracker(status_msg, "File is downloading") if status_msg else None

    def hook(d):
        if d.get("status") == "downloading" and tracker:
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            tracker.update(d.get("downloaded_bytes", 0), total)

    ydl_opts = {
        # --- format / merge ---
        "format": "bv*+ba/b",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "merge_output_format": "mkv",

        # --- ffmpeg ---
        "ffmpeg_location": ffmpeg_path,   # exact binary
        # (yt-dlp ffmpeg_location e binary path o accept kore,
        #  kintu kichu version e directory expect kore — niche fallback o rakhi)

        # --- speed ---
        "concurrent_fragment_downloads": FRAGMENT_WORKERS,
        "retries": 5,
        "fragment_retries": 10,

        # --- quiet ---
        "quiet": True,
        "noprogress": True,
        "no_warnings": True,

        # --- progress ---
        "progress_hooks": [hook],
    }

    # kichu yt-dlp version e ffmpeg_location directory expect kore,
    # tai jodi binary path fail kore tahole directory diye retry korbo
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = ydl.prepare_filename(info)
    except yt_dlp.utils.DownloadError:
        # fallback: directory path
        ydl_opts["ffmpeg_location"] = ffmpeg_dir
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = ydl.prepare_filename(info)

    # prepare_filename ext mkv na-o hote pare — actual file khuje ber kori
    if not os.path.exists(path):
        base = os.path.splitext(path)[0]
        for ext in (".mkv", ".mp4", ".webm", ".flv"):
            candidate = base + ext
            if os.path.exists(candidate):
                return candidate

    return path
