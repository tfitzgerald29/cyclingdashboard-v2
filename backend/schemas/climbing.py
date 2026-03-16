"""
Schema for rock climbing session_mesgs rows
(sport == "rock_climbing").

The climbing tab also reads split_mesgs directly; those columns are
covered by base.SPLIT_BASE.
"""

import polars as pl

from .base import SESSION_BASE

SESSION: dict[str, pl.DataType] = {
    **SESSION_BASE,
    # Rock-climbing-specific fields (may be absent on older activities)
    "total_cycles": pl.Float64,  # total moves/pulls
    "total_grit": pl.Float64,  # Garmin route difficulty metric
}
