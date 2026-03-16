"""
Columns shared by every sport's session_mesgs rows.

These are the fields that every FIT activity produces regardless of sport,
plus the pipeline-injected ``source_file`` column.  Per-sport schemas extend
this dict with their own sport-specific columns.
"""

import polars as pl

# ── session_mesgs base columns ────────────────────────────────────────────────

SESSION_BASE: dict[str, pl.DataType] = {
    # Identity / provenance
    "source_file": pl.Utf8,
    "sport": pl.Utf8,
    "sub_sport": pl.Utf8,
    "sport_profile_name": pl.Utf8,
    # Timing
    "timestamp": pl.Datetime("us", "UTC"),
    "start_time": pl.Datetime("us", "UTC"),
    "total_elapsed_time": pl.Float64,  # seconds
    "total_timer_time": pl.Float64,  # seconds (moving timer)
    "total_moving_time": pl.Float64,  # seconds
    # Distance / speed
    "total_distance": pl.Float64,  # metres
    "avg_speed": pl.Float64,  # m/s
    "max_speed": pl.Float64,  # m/s
    "enhanced_avg_speed": pl.Float64,  # m/s (higher-res)
    "enhanced_max_speed": pl.Float64,  # m/s (higher-res)
    # Elevation
    "total_ascent": pl.Float64,  # metres
    "total_descent": pl.Float64,  # metres
    "total_fractional_ascent": pl.Float64,
    "total_fractional_descent": pl.Float64,
    # Heart rate
    "avg_heart_rate": pl.Float64,  # bpm
    "max_heart_rate": pl.Float64,  # bpm
    # GPS bounding box
    "nec_lat": pl.Float64,
    "nec_long": pl.Float64,
    "swc_lat": pl.Float64,
    "swc_long": pl.Float64,
    "start_position_lat": pl.Float64,
    "start_position_long": pl.Float64,
    "end_position_lat": pl.Float64,
    "end_position_long": pl.Float64,
    # Laps / events
    "num_laps": pl.Float64,
    "first_lap_index": pl.Float64,
    "message_index": pl.Float64,
    "event": pl.Utf8,
    "event_type": pl.Utf8,
    "event_group": pl.Float64,
    "trigger": pl.Utf8,
    # Calories / output
    "total_calories": pl.Float64,  # kcal
    "total_fat_calories": pl.Float64,
    "metabolic_calories": pl.Float64,  # Garmin metabolic (non-exercise) calories
    "total_strokes": pl.Float64,  # paddle/ski strokes — present across multiple sports
    # Training effect
    "total_training_effect": pl.Float64,
    "total_anaerobic_training_effect": pl.Float64,
    "training_load_peak": pl.Float64,
    # Temperature
    "avg_temperature": pl.Float64,  # °C
    "max_temperature": pl.Float64,
    "min_temperature": pl.Float64,
    # Cadence / gait (cross-sport)
    "avg_fractional_cadence": pl.Float64,
    # Flow / grade score (cycling + skiing + climbing)
    "avg_flow": pl.Float64,
    "avg_vam": pl.Float64,  # vertical ascent metres/hour — cycling + hiking
    # Respiration (HRV/respiration sensor)
    "enhanced_avg_respiration_rate": pl.Float64,
    "enhanced_max_respiration_rate": pl.Float64,
    "enhanced_min_respiration_rate": pl.Float64,
}

# ── record_mesgs base columns ─────────────────────────────────────────────────

RECORD_BASE: dict[str, pl.DataType] = {
    "source_file": pl.Utf8,
    "timestamp": pl.Datetime("us", "UTC"),
    "distance": pl.Float64,  # metres
    "speed": pl.Float64,  # m/s
    "enhanced_speed": pl.Float64,
    "altitude": pl.Float64,  # metres
    "enhanced_altitude": pl.Float64,
    "heart_rate": pl.Float64,  # bpm
    "cadence": pl.Float64,
    "fractional_cadence": pl.Float64,
    "temperature": pl.Float64,  # °C
    "position_lat": pl.Float64,  # semicircles (raw FIT)
    "position_long": pl.Float64,
    "activity_type": pl.Utf8,
}

# ── split_mesgs base columns ──────────────────────────────────────────────────

SPLIT_BASE: dict[str, pl.DataType] = {
    "source_file": pl.Utf8,
    "split_type": pl.Utf8,
    "message_index": pl.Float64,
    "start_time": pl.Datetime("us", "UTC"),
    "end_time": pl.Datetime("us", "UTC"),
    "total_elapsed_time": pl.Float64,
    "total_timer_time": pl.Float64,
    "total_moving_time": pl.Float64,
    "total_distance": pl.Float64,
    "total_ascent": pl.Float64,
    "total_descent": pl.Float64,
    "total_calories": pl.Float64,
    "avg_speed": pl.Float64,
    "max_speed": pl.Float64,
    "avg_vert_speed": pl.Float64,
    "start_elevation": pl.Float64,
    "start_position_lat": pl.Float64,
    "start_position_long": pl.Float64,
    "end_position_lat": pl.Float64,
    "end_position_long": pl.Float64,
}

# ── split_summary_mesgs base columns ─────────────────────────────────────────

SPLIT_SUMMARY_BASE: dict[str, pl.DataType] = {
    "source_file": pl.Utf8,
    "split_type": pl.Utf8,
    "message_index": pl.Float64,
    "num_splits": pl.Float64,
    "total_timer_time": pl.Float64,
    "total_moving_time": pl.Float64,
    "total_distance": pl.Float64,
    "total_ascent": pl.Float64,
    "total_descent": pl.Float64,
    "total_calories": pl.Float64,
    "avg_speed": pl.Float64,
    "max_speed": pl.Float64,
    "avg_vert_speed": pl.Float64,
    "avg_heart_rate": pl.Float64,
    "max_heart_rate": pl.Float64,
}
