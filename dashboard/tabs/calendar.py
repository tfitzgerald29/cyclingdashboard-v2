import json

from dash import html

from backend.sleep_processor import SleepProcessor
from backend.SportSummarizer import SportSummarizer
from ..config import CARD_STYLE, COLORS

# Sport → display color — kept here for the legend rendering
SPORT_COLORS = {
    "cycling": "#2196F3",
    "weight_lifting": "#FF9800",
    "rock_climbing": "#4CAF50",
    "running": "#E91E63",
    "hiking": "#8BC34A",
    "alpine_skiing": "#00BCD4",
}


def _load_events(user_id=None):
    """Load all activities and return (events_list, raw_rows_for_totals)."""
    return SportSummarizer(user_id=user_id).get_calendar_events()


def _load_sleep(user_id=None) -> dict:
    """Return {calendar_date: score_overall} for all nights with a score."""
    sp = SleepProcessor(user_id=user_id)
    if sp.sleep.is_empty():
        return {}
    df = sp.sleep.select(["calendar_date", "score_overall"]).drop_nulls()
    return {row["calendar_date"]: row["score_overall"] for row in df.to_dicts()}


def calendar_tab(user_id=None):
    events, raw = _load_events(user_id)
    sleep_scores = _load_sleep(user_id)

    # Find the latest event date so the calendar opens to the right month
    latest_date = max((e["start"] for e in events), default=None) if events else None

    return html.Div(
        [
            # Data for JS to read
            html.Script(
                id="fc-events-data",
                type="application/json",
                children=json.dumps(events),
            ),
            html.Script(
                id="fc-raw-data", type="application/json", children=json.dumps(raw)
            ),
            html.Script(
                id="fc-initial-date",
                type="application/json",
                children=json.dumps(latest_date),
            ),
            html.Script(
                id="fc-sleep-data",
                type="application/json",
                children=json.dumps(sleep_scores),
            ),
            html.Div(
                style={**CARD_STYLE},
                children=[
                    html.Div(id="fc-container"),
                ],
            ),
            # Legend
            html.Div(
                style={
                    "display": "flex",
                    "gap": "16px",
                    "flexWrap": "wrap",
                    "marginTop": "8px",
                },
                children=[
                    html.Div(
                        style={"display": "flex", "alignItems": "center", "gap": "6px"},
                        children=[
                            html.Div(
                                style={
                                    "width": "12px",
                                    "height": "12px",
                                    "borderRadius": "2px",
                                    "backgroundColor": color,
                                }
                            ),
                            html.Span(
                                label,
                                style={
                                    "fontSize": "0.8rem",
                                    "color": COLORS["muted"],
                                },
                            ),
                        ],
                    )
                    for label, color in [
                        ("Cycling", SPORT_COLORS["cycling"]),
                        ("Lifting", SPORT_COLORS["weight_lifting"]),
                        ("Rock Climbing", SPORT_COLORS["rock_climbing"]),
                        ("Running", SPORT_COLORS["running"]),
                        ("Hiking", SPORT_COLORS["hiking"]),
                        ("Skiing", SPORT_COLORS["alpine_skiing"]),
                        ("Sleep Score", "#00BCD4"),
                    ]
                ],
            ),
        ]
    )
