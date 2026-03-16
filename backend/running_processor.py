"""
Read-only query layer for running sessions.

Does not inherit from FitFileProcessor — FIT ingestion is handled
separately at startup via FitFileProcessor.run() in app.py.
"""

import os

import polars as pl

from .schemas import load_sessions

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_MERGED_PATH = os.path.join(_BASE_DIR, "mergedfiles")


class RunningProcessor:
    def __init__(self, mergedfiles_path=None) -> None:
        self.mergedfiles_path = mergedfiles_path or _DEFAULT_MERGED_PATH
        self.running = self._load_running_sessions()

    def _load_running_sessions(self) -> pl.DataFrame:
        parquet_path = os.path.join(self.mergedfiles_path, "session_mesgs.parquet")
        df = load_sessions("running", parquet_path)
        if df.is_empty():
            return df
        ts_col = "timestamp"
        if df[ts_col].dtype.time_zone is None:
            df = df.with_columns(pl.col(ts_col).dt.replace_time_zone("UTC"))
        return df.with_columns(
            pl.col(ts_col).dt.convert_time_zone("America/Denver").alias(ts_col)
        )

    def list_runs(self) -> list[dict]:
        """Return runs sorted most-recent-first for a dropdown."""
        df = self.running.sort("timestamp", descending=True)
        result = []
        for r in df.to_dicts():
            dt = r["timestamp"]
            dist_mi = (
                round(r["total_distance"] / 1609.344, 2)
                if r.get("total_distance")
                else 0
            )
            label = f"{dt.strftime('%Y-%m-%d')} — {dist_mi} mi"
            result.append({"label": label, "value": r["source_file"]})
        return result

    def summary_stats(self) -> dict:
        """High-level totals across all runs."""
        df = self.running
        if df.is_empty():
            return {}
        return {
            "total_runs": len(df),
            "total_miles": round(df["total_distance"].drop_nulls().sum() / 1609.344, 1),
            "total_hours": round(df["total_timer_time"].sum() / 3600, 1),
        }
