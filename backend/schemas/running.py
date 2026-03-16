"""
Schema for running session_mesgs rows (sport == "running").
"""

import polars as pl

from .base import RECORD_BASE, SESSION_BASE

SESSION: dict[str, pl.DataType] = {
    **SESSION_BASE,
    # Running-specific
    "training_stress_score": pl.Float64,
    "intensity_factor": pl.Float64,
    "avg_step_length": pl.Float64,  # mm
    "total_strides": pl.Float64,
    "avg_running_cadence": pl.Float64,
    "max_running_cadence": pl.Float64,
    "avg_cadence": pl.Float64,  # steps/min (half-cadence in FIT)
    "max_cadence": pl.Float64,
    "avg_stance_time": pl.Float64,  # ms
    "avg_vertical_oscillation": pl.Float64,  # mm
    "avg_vertical_ratio": pl.Float64,  # %
}

RECORD: dict[str, pl.DataType] = {
    **RECORD_BASE,
    "vertical_oscillation": pl.Float64,
    "vertical_ratio": pl.Float64,
    "stance_time": pl.Float64,
    "step_length": pl.Float64,
    "cycles": pl.Float64,
}
