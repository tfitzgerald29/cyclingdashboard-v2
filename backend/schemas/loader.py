"""
Schema-safe parquet loader.

``load_sessions(sport, parquet_path)`` reads session_mesgs.parquet,
filters to the requested sport, and coerces every column to the declared
dtype from the sport's schema.  Missing columns are added as null columns
with the correct type; unexpected columns are left untouched.

Any coercion failure is **logged explicitly** instead of silently falling
back to a supertype — which was the root cause of the schema drift that
motivated this refactor.
"""

import polars as pl

from . import climbing, cycling, hiking, running, skiing
from .base import RECORD_BASE, SPLIT_BASE, SPLIT_SUMMARY_BASE
from ..storage import storage

# ── Sport → FIT sport string(s) ──────────────────────────────────────────────

_SPORT_FILTER: dict[str, list[str]] = {
    "cycling": ["cycling"],
    "skiing": ["alpine_skiing"],
    "climbing": ["rock_climbing"],
    "running": ["running"],
    "hiking": ["hiking"],
}

# ── Sport → SESSION schema dict ───────────────────────────────────────────────

_SESSION_SCHEMA: dict[str, dict[str, pl.DataType]] = {
    "cycling": cycling.SESSION,
    "skiing": skiing.SESSION,
    "climbing": climbing.SESSION,
    "running": running.SESSION,
    "hiking": hiking.SESSION,
}

# ── Sport → RECORD schema dict (cycling only for now) ────────────────────────

_RECORD_SCHEMA: dict[str, dict[str, pl.DataType]] = {
    "cycling": cycling.RECORD,
    "running": running.RECORD,
    "hiking": hiking.RECORD,
}


# ── Internal helpers ──────────────────────────────────────────────────────────


def _coerce_df(
    df: pl.DataFrame,
    schema: dict[str, pl.DataType],
    context: str,
) -> pl.DataFrame:
    """Apply *schema* to *df*: add missing columns as null, cast mismatches.

    Parameters
    ----------
    df:
        The DataFrame to coerce.
    schema:
        Mapping of column name → target Polars dtype.
    context:
        Human-readable label used in log messages (e.g. "cycling/session").

    Returns
    -------
    pl.DataFrame
        A new DataFrame with every schema column present and correctly typed.
        Columns not listed in *schema* are passed through unchanged.
    """
    for col, dtype in schema.items():
        if col not in df.columns:
            # Column is entirely absent — add as all-null with correct dtype.
            # Use pl.Series to avoid the 1-row expansion that pl.lit(None) triggers
            # on an empty DataFrame.
            null_series = pl.Series(col, [None] * len(df), dtype=dtype)
            df = df.with_columns(null_series)
        elif df[col].dtype != dtype:
            actual = df[col].dtype
            try:
                df = df.with_columns(pl.col(col).cast(dtype))
            except Exception as exc:
                print(
                    f"  [schema/{context}] WARNING: cannot cast '{col}' "
                    f"from {actual} → {dtype}: {exc}. Column left as-is."
                )

    return df


# ── Public API ────────────────────────────────────────────────────────────────


def load_sessions(
    sport: str,
    parquet_path: str,
) -> pl.DataFrame:
    """Load and schema-coerce session rows for *sport* from *parquet_path*.

    Parameters
    ----------
    sport:
        One of ``"cycling"``, ``"skiing"``, ``"climbing"``, ``"running"``,
        ``"hiking"``.
    parquet_path:
        Absolute path to ``session_mesgs.parquet``.

    Returns
    -------
    pl.DataFrame
        Filtered to the sport, with all schema columns guaranteed present and
        correctly typed.  Returns an empty DataFrame if the file doesn't exist
        or the sport has no rows.
    """
    sport_values = _SPORT_FILTER.get(sport)
    if sport_values is None:
        raise ValueError(
            f"Unknown sport '{sport}'. Known sports: {list(_SPORT_FILTER.keys())}"
        )

    schema = _SESSION_SCHEMA[sport]

    if not storage.path_exists(parquet_path):
        return _coerce_df(pl.DataFrame(), schema, f"{sport}/session")

    df = storage.read_parquet(parquet_path).filter(pl.col("sport").is_in(sport_values))
    return _coerce_df(df, schema, f"{sport}/session")


def load_records(
    sport: str,
    parquet_path: str,
    source_files: list[str] | None = None,
    columns: list[str] | None = None,
) -> pl.DataFrame:
    """Load and schema-coerce record rows for *sport* from *parquet_path*.

    Parameters
    ----------
    sport:
        Sport key (only ``"cycling"``, ``"running"``, ``"hiking"`` have
        record schemas defined; others fall back to ``RECORD_BASE``).
    parquet_path:
        Absolute path to ``record_mesgs.parquet``.
    source_files:
        If provided, filter to only these source files before coercion
        (avoids loading the full record table when only one ride is needed).
    columns:
        If provided, only read these columns from the parquet file
        (passed directly to ``pl.read_parquet``).

    Returns
    -------
    pl.DataFrame
        Schema-coerced record rows.
    """
    schema = _RECORD_SCHEMA.get(sport, RECORD_BASE)

    if not storage.path_exists(parquet_path):
        return _coerce_df(pl.DataFrame(), schema, f"{sport}/record")

    read_kwargs: dict = {}
    if columns is not None:
        read_kwargs["columns"] = columns

    df = storage.read_parquet(parquet_path, **read_kwargs)

    if source_files is not None:
        df = df.filter(pl.col("source_file").is_in(source_files))

    return _coerce_df(df, schema, f"{sport}/record")


def load_splits(
    parquet_path: str,
    source_files: list[str] | None = None,
) -> pl.DataFrame:
    """Load and schema-coerce split_mesgs from *parquet_path*.

    Parameters
    ----------
    parquet_path:
        Absolute path to ``split_mesgs.parquet``.
    source_files:
        If provided, filter to only these source files.
    """
    if not storage.path_exists(parquet_path):
        return _coerce_df(pl.DataFrame(), SPLIT_BASE, "split")

    df = storage.read_parquet(parquet_path)

    if source_files is not None:
        df = df.filter(pl.col("source_file").is_in(source_files))

    return _coerce_df(df, SPLIT_BASE, "split")


def load_split_summaries(
    parquet_path: str,
    source_files: list[str] | None = None,
) -> pl.DataFrame:
    """Load and schema-coerce split_summary_mesgs from *parquet_path*."""
    if not storage.path_exists(parquet_path):
        return _coerce_df(pl.DataFrame(), SPLIT_SUMMARY_BASE, "split_summary")

    df = storage.read_parquet(parquet_path)

    if source_files is not None:
        df = df.filter(pl.col("source_file").is_in(source_files))

    return _coerce_df(df, SPLIT_SUMMARY_BASE, "split_summary")
