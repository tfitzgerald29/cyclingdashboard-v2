from dash import Input, Output, State, callback, no_update

from backend.auth import get_supabase_client
from backend.storage import storage

from .auth_layout import login_layout
from .tabs import (
    calendar_tab,
    climbing_tab,
    cycling_tab,
    hiking_tab,
    pickleball_tab,
    running_tab,
    skiing_tab,
    sleep_tab,
    sports_tab,
    upload_tab,
    weights_tab,
)
from .config import get_user_id


# ── Email / password auth callbacks ──────────────────────────────────────────
@callback(
    Output("user-store", "data", allow_duplicate=True),
    Output("auth-message", "children"),
    Output("auth-message", "style"),
    Input("btn-signin", "n_clicks"),
    State("auth-email", "value"),
    State("auth-password", "value"),
    prevent_initial_call=True,
)
def handle_signin(n_clicks, email, password):
    if not n_clicks or not email or not password:
        return no_update, no_update, no_update
    try:
        sb = get_supabase_client()
        resp = sb.auth.sign_in_with_password({"email": email, "password": password})
        user = resp.user
        return (
            {"user_id": user.id, "email": user.email},
            "",
            {},
        )
    except Exception as e:
        return (
            no_update,
            str(e),
            {"color": "#f44336", "marginBottom": "12px", "fontSize": "0.88rem"},
        )


@callback(
    Output("user-store", "data", allow_duplicate=True),
    Output("auth-message", "children", allow_duplicate=True),
    Output("auth-message", "style", allow_duplicate=True),
    Input("btn-signup", "n_clicks"),
    State("auth-email", "value"),
    State("auth-password", "value"),
    prevent_initial_call=True,
)
def handle_signup(n_clicks, email, password):
    if not n_clicks or not email or not password:
        return no_update, no_update, no_update
    try:
        sb = get_supabase_client()
        resp = sb.auth.sign_up({"email": email, "password": password})
        user = resp.user
        if user and user.identities:
            return (
                {"user_id": user.id, "email": user.email},
                "",
                {},
            )
        return (
            no_update,
            "Account created — check your email to confirm before signing in.",
            {"color": "#4CAF50", "marginBottom": "12px", "fontSize": "0.88rem"},
        )
    except Exception as e:
        return (
            no_update,
            str(e),
            {"color": "#f44336", "marginBottom": "12px", "fontSize": "0.88rem"},
        )


# ── Tab router ────────────────────────────────────────────────────────────────
# Listens to both tab switches AND user-store changes so the dashboard renders
# immediately after a successful login without requiring a tab click.
@callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
    Input("user-store", "data"),
)
def render_tab(tab, user_data):
    if storage.is_s3() and (not user_data or not user_data.get("user_id")):
        return login_layout()

    uid = get_user_id(user_data)

    if tab == "upload":
        return upload_tab()
    elif tab == "calendar":
        return calendar_tab(user_id=uid)
    elif tab == "cycling":
        return cycling_tab()
    elif tab == "climbing":
        return climbing_tab()
    elif tab == "hiking":
        return hiking_tab()
    elif tab == "running":
        return running_tab()
    elif tab == "pickleball":
        return pickleball_tab()
    elif tab == "sports":
        return sports_tab()
    elif tab == "weights":
        return weights_tab(user_id=uid)
    elif tab == "Ski":
        return skiing_tab()
    elif tab == "sleep":
        return sleep_tab()
