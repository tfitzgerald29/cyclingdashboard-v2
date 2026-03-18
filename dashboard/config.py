import os

from backend.storage import storage

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# These are only valid in local mode. In S3 mode, paths are resolved
# per-user at callback time via storage.merged_path(user_id).
MERGED_PATH = storage.merged_path() if not storage.is_s3() else ""
WT_DATA_FILE = storage.wt_data_file() if not storage.is_s3() else ""
WT_DRAFT_FILE = storage.wt_draft_file() if not storage.is_s3() else ""
BODY_WEIGHT_LB = 133


def get_user_id(user_data: dict | None) -> str | None:
    """Extract user_id from dcc.Store data, or None in local mode."""
    if not storage.is_s3():
        return None
    if not user_data:
        return None
    return user_data.get("user_id")


COLORS = {
    "bg": "#0f1117",
    "card": "#1a1d27",
    "border": "#2a2d37",
    "text": "#e0e0e0",
    "muted": "#888",
    "accent": "#2196F3",
}

CARD_STYLE = {
    "backgroundColor": COLORS["card"],
    "border": f"1px solid {COLORS['border']}",
    "borderRadius": "8px",
    "padding": "16px",
    "marginBottom": "16px",
}
