"""
Schema for cycling session_mesgs rows (sport == "cycling").

Extends SESSION_BASE with cycling-specific power, cadence, and balance fields.
"""

import polars as pl

from .base import RECORD_BASE, SESSION_BASE

SESSION: dict[str, pl.DataType] = {
    **SESSION_BASE,
    # Power
    "avg_power": pl.Float64,  # watts
    "max_power": pl.Float64,
    "normalized_power": pl.Float64,
    "threshold_power": pl.Float64,  # FTP at time of activity
    "total_work": pl.Float64,  # joules
    # Training load
    "training_stress_score": pl.Float64,
    "intensity_factor": pl.Float64,
    # Cadence
    "avg_cadence": pl.Float64,  # rpm
    "max_cadence": pl.Float64,
    "avg_cadence_position": pl.Float64,
    "max_cadence_position": pl.Float64,
    "max_fractional_cadence": pl.Float64,
    # Balance / pedalling
    "left_right_balance": pl.Float64,  # Garmin bitmask
    "avg_combined_pedal_smoothness": pl.Float64,
    "avg_left_pedal_smoothness": pl.Float64,
    "avg_right_pedal_smoothness": pl.Float64,
    "avg_left_torque_effectiveness": pl.Float64,
    "avg_right_torque_effectiveness": pl.Float64,
    "avg_left_pco": pl.Float64,  # platform centre offset
    "avg_right_pco": pl.Float64,
    "max_power_position": pl.Float64,
    "stand_count": pl.Float64,
    "time_standing": pl.Float64,  # seconds spent out of saddle
    "total_grit": pl.Float64,
    "total_cycles": pl.Float64,
}

RECORD: dict[str, pl.DataType] = {
    **RECORD_BASE,
    "power": pl.Float64,  # watts (cast to Int64 when used)
    "accumulated_power": pl.Float64,
    "compressed_accumulated_power": pl.Float64,
    "left_pedal_smoothness": pl.Float64,
    "right_pedal_smoothness": pl.Float64,
    "left_torque_effectiveness": pl.Float64,
    "right_torque_effectiveness": pl.Float64,
    "left_pco": pl.Float64,
    "right_pco": pl.Float64,
    "combined_pedal_smoothness": pl.Float64,
    "left_right_balance": pl.Float64,
    "resistance": pl.Float64,
    "cycles": pl.Float64,
    "cycle_length16": pl.Float64,
    "vertical_oscillation": pl.Float64,
    "vertical_ratio": pl.Float64,
    "stance_time": pl.Float64,
    "step_length": pl.Float64,
    "enhanced_respiration_rate": pl.Float64,
    "flow": pl.Float64,
    "grit": pl.Float64,
}
