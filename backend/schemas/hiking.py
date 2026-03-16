"""
Schema for hiking session_mesgs rows (sport == "hiking").
"""

import polars as pl

from .base import RECORD_BASE, SESSION_BASE

SESSION: dict[str, pl.DataType] = {
    **SESSION_BASE,
    # Hiking shares the same fields as running for now; extend as needed
    "training_stress_score": pl.Float64,
    "avg_step_length": pl.Float64,
    "total_strides": pl.Float64,
    "max_running_cadence": pl.Float64,
    "avg_cadence": pl.Float64,
    "max_cadence": pl.Float64,
}

RECORD: dict[str, pl.DataType] = {
    **RECORD_BASE,
    "vertical_oscillation": pl.Float64,
    "stance_time": pl.Float64,
    "step_length": pl.Float64,
    "cycles": pl.Float64,
}
