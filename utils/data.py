"""Database helpers – all writes use the admin (service-role) client."""
from datetime import datetime, timezone

import streamlit as st

from .supabase_client import get_admin_supabase
from .scoring import calculate_match_points


# ── Matches ──────────────────────────────────────────────────────────────────

def get_all_matches() -> list[dict]:
    client = get_admin_supabase()
    result = (
        client.table("matches")
        .select("*")
        .order("match_date")
        .execute()
    )
    return result.data or []


def get_matches_by_group(group: str) -> list[dict]:
    client = get_admin_supabase()
    result = (
        client.table("matches")
        .select("*")
        .eq("group_name", group)
        .order("match_date")
        .execute()
    )
    return result.data or []


# ── Predictions ───────────────────────────────────────────────────────────────

def get_user_predictions(user_id: str) -> dict[int, dict]:
    """Returns {match_id: prediction_row}."""
    client = get_admin_supabase()
    result = (
        client.table("predictions")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    return {row["match_id"]: row for row in (result.data or [])}


def save_prediction(
    user_id: str,
    match_id: int,
    pred_a: int,
    pred_b: int,
    pred_penalties: bool = False,
    pred_pen_a: int | None = None,
    pred_pen_b: int | None = None,
) -> bool:
    client = get_admin_supabase()
    now = datetime.now(timezone.utc).isoformat()
    row: dict = {
        "user_id": user_id,
        "match_id": match_id,
        "pred_a": pred_a,
        "pred_b": pred_b,
        "pred_penalties": pred_penalties,
        "pred_pen_a": pred_pen_a if pred_penalties else None,
        "pred_pen_b": pred_pen_b if pred_penalties else None,
        "points": 0,
        "updated_at": now,
    }
    try:
        client.table("predictions").upsert(row, on_conflict="user_id,match_id").execute()
        return True
    except Exception:
        return False


# ── Ranking ───────────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def get_ranking() -> list[dict]:
    client = get_admin_supabase()
    profiles = client.table("profiles").select("id, nickname, department, shift").execute().data or []
    if not profiles:
        return []

    finished_matches = [m for m in get_all_matches() if m.get("finished")]
    user_pts: dict[str, int] = {}
    for match in finished_matches:
        preds = (
            client.table("predictions")
            .select("user_id, points")
            .eq("match_id", match["id"])
            .execute()
            .data or []
        )
        for p in preds:
            uid = p["user_id"]
            user_pts[uid] = user_pts.get(uid, 0) + (p["points"] or 0)

    ranking = []
    for prof in profiles:
        uid = prof["id"]
        ranking.append(
            {
                "nickname": prof["nickname"],
                "department": prof.get("department") or "—",
                "shift": prof.get("shift") or "—",
                "total_points": user_pts.get(uid, 0),
            }
        )

    ranking.sort(key=lambda x: x["total_points"], reverse=True)
    return ranking


# ── Admin ─────────────────────────────────────────────────────────────────────

def update_match_result(
    match_id: int,
    result_a: int,
    result_b: int,
    result_penalties: bool = False,
    result_pen_a: int | None = None,
    result_pen_b: int | None = None,
) -> bool:
    client = get_admin_supabase()
    try:
        client.table("matches").update({
            "result_a": result_a,
            "result_b": result_b,
            "finished": True,
            "result_penalties": result_penalties,
            "result_pen_a": result_pen_a if result_penalties else None,
            "result_pen_b": result_pen_b if result_penalties else None,
        }).eq("id", match_id).execute()
        _recalculate_match_points(
            match_id, result_a, result_b,
            result_penalties, result_pen_a, result_pen_b,
        )
        get_ranking.clear()
        get_all_predictions_with_profiles.clear()
        return True
    except Exception:
        return False


def _recalculate_match_points(
    match_id: int,
    result_a: int,
    result_b: int,
    result_penalties: bool = False,
    result_pen_a: int | None = None,
    result_pen_b: int | None = None,
) -> None:
    client = get_admin_supabase()
    preds = (
        client.table("predictions")
        .select("id, pred_a, pred_b, pred_penalties, pred_pen_a, pred_pen_b")
        .eq("match_id", match_id)
        .execute()
        .data or []
    )
    for pred in preds:
        pts = calculate_match_points(
            pred["pred_a"], pred["pred_b"], result_a, result_b,
            pred_penalties=bool(pred.get("pred_penalties")),
            pred_pen_a=pred.get("pred_pen_a"),
            pred_pen_b=pred.get("pred_pen_b"),
            result_penalties=result_penalties,
            result_pen_a=result_pen_a,
            result_pen_b=result_pen_b,
        )
        client.table("predictions").update({"points": pts}).eq("id", pred["id"]).execute()


@st.cache_data(ttl=300)
def get_all_predictions_with_profiles() -> dict[int, list[dict]]:
    """Returns {match_id: [{nickname, pred_a, pred_b, points}]}."""
    client = get_admin_supabase()
    matches = get_all_matches()
    if not matches:
        return {}

    profiles_data = client.table("profiles").select("id, nickname").execute().data or []
    profiles = {p["id"]: p["nickname"] for p in profiles_data}
    if not profiles:
        return {}

    result: dict[int, list[dict]] = {}
    for match in matches:
        mid = match["id"]
        preds = (
            client.table("predictions")
            .select("user_id, pred_a, pred_b, points")
            .eq("match_id", mid)
            .execute()
            .data or []
        )
        if preds:
            result[mid] = [
                {
                    "nickname": profiles.get(p["user_id"], "?"),
                    "pred_a": p["pred_a"],
                    "pred_b": p["pred_b"],
                    "points": p["points"] or 0,
                }
                for p in preds
            ]
    return result


def get_predictions_for_match(match_id: int) -> list[dict]:
    """Returns all users' predictions for a given match (for admin view)."""
    client = get_admin_supabase()
    preds = (
        client.table("predictions")
        .select("user_id, pred_a, pred_b, points")
        .eq("match_id", match_id)
        .execute()
        .data or []
    )
    profiles = {
        p["id"]: p["nickname"]
        for p in (client.table("profiles").select("id, nickname").execute().data or [])
    }
    return [
        {
            "nickname": profiles.get(p["user_id"], p["user_id"]),
            "pred_a": p["pred_a"],
            "pred_b": p["pred_b"],
            "points": p["points"],
        }
        for p in preds
    ]


def get_orphaned_predictions() -> list[dict]:
    """Returns data for user_ids that have predictions but no profiles row."""
    client = get_admin_supabase()
    profile_ids = {p["id"] for p in (client.table("profiles").select("id").execute().data or [])}
    preds = client.table("predictions").select("user_id, points").gte("match_id", 1).execute().data or []

    user_data: dict[str, dict] = {}
    for p in preds:
        uid = p["user_id"]
        if uid not in user_data:
            user_data[uid] = {"user_id": uid, "pred_count": 0, "total_points": 0}
        user_data[uid]["pred_count"] += 1
        user_data[uid]["total_points"] += p["points"] or 0

    return [v for uid, v in user_data.items() if uid not in profile_ids]


def create_missing_profile(user_id: str, nickname: str, department: str, shift: str) -> bool:
    client = get_admin_supabase()
    try:
        client.table("profiles").insert({
            "id": user_id,
            "nickname": nickname.strip(),
            "department": department,
            "shift": shift,
        }).execute()
        return True
    except Exception:
        return False


def seed_matches_if_empty() -> None:
    """Insert all 72 fixtures if the matches table is empty."""
    from data.matches import get_all_fixtures

    client = get_admin_supabase()
    existing = client.table("matches").select("id").limit(1).execute()
    if existing.data:
        return
    fixtures = get_all_fixtures()
    rows = [
        {
            "group_name": f["group_name"],
            "team_a": f["team_a"],
            "team_b": f["team_b"],
            "match_date": f["match_date"],
            "stage": f["stage"],
        }
        for f in fixtures
    ]
    client.table("matches").insert(rows).execute()


def seed_playoffs_if_empty() -> tuple[bool, int]:
    """Insert the 32 knockout fixtures if none exist yet. Returns (ok, count_inserted)."""
    from data.matches import get_playoff_fixtures

    client = get_admin_supabase()
    existing = (
        client.table("matches")
        .select("id")
        .neq("stage", "group")
        .limit(1)
        .execute()
    )
    if existing.data:
        return False, 0
    fixtures = get_playoff_fixtures()
    rows = [
        {
            "group_name": f["group_name"],
            "team_a": f["team_a"],
            "team_b": f["team_b"],
            "match_date": f["match_date"],
            "stage": f["stage"],
        }
        for f in fixtures
    ]
    client.table("matches").insert(rows).execute()
    return True, len(rows)


def get_playoff_matches() -> list[dict]:
    """Return all knockout-stage matches ordered by date."""
    client = get_admin_supabase()
    result = (
        client.table("matches")
        .select("*")
        .neq("stage", "group")
        .order("match_date")
        .execute()
    )
    return result.data or []


def update_match_teams(match_id: int, team_a: str, team_b: str) -> bool:
    client = get_admin_supabase()
    try:
        client.table("matches").update(
            {"team_a": team_a.strip(), "team_b": team_b.strip()}
        ).eq("id", match_id).execute()
        return True
    except Exception:
        return False


def update_match_datetime(match_id: int, new_utc_iso: str) -> bool:
    client = get_admin_supabase()
    try:
        client.table("matches").update({"match_date": new_utc_iso}).eq("id", match_id).execute()
        return True
    except Exception:
        return False


def reseed_matches() -> bool:
    """Delete all predictions and matches, then re-insert official fixtures."""
    from data.matches import get_all_fixtures

    client = get_admin_supabase()
    try:
        client.table("predictions").delete().neq("id", 0).execute()
        client.table("matches").delete().neq("id", 0).execute()
        fixtures = get_all_fixtures()
        rows = [
            {
                "group_name": f["group_name"],
                "team_a": f["team_a"],
                "team_b": f["team_b"],
                "match_date": f["match_date"],
                "stage": f["stage"],
            }
            for f in fixtures
        ]
        client.table("matches").insert(rows).execute()
        return True
    except Exception:
        return False
