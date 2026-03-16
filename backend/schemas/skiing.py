"""
Schema for alpine skiing session_mesgs rows
(sport == "alpine_skiing").

The skiing processor selects 22 specific columns.  This schema covers
all of them so the loader can guarantee their presence and type.
"""

import polars as pl

from .base import SESSION_BASE

SESSION: dict[str, pl.DataType] = {
    **SESSION_BASE,
    # Laps (runs down the mountain)
    "num_laps": pl.Float64,  # already in base; explicit for clarity
}
