"""Database helpers – all writes use the admin (service-role) client."""
from datetime import datetime, timezone

import streamlit as st

from .supabase_client import get_admin_supabase
from .scoring import calculate_match_points, calculate_special_points


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


def save_prediction(user_id: str, match_id: int, pred_a: int, pred_b: int) -> bool:
    client = get_admin_supabase()
    now = datetime.now(timezone.utc).isoformat()
    try:
        client.table("predictions").upsert(
            {
                "user_id": user_id,
                "match_id": match_id,
                "pred_a": pred_a,
                "pred_b": pred_b,
                "points": 0,
                "updated_at": now,
            },
            on_conflict="user_id,match_id",
        ).execute()
        return True
    except Exception:
        return False


# ── Special predictions ───────────────────────────────────────────────────────

def get_special_prediction(user_id: str) -> dict | None:
    client = get_admin_supabase()
    try:
        result = (
            client.table("special_predictions")
            .select("*")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
        return result.data[0] if result.data else None
    except Exception:
        return None


def save_special_prediction(user_id: str, artilheiro: str, mvp: str, goleiro: str) -> bool:
    client = get_admin_supabase()
    now = datetime.now(timezone.utc).isoformat()
    try:
        client.table("special_predictions").upsert(
            {
                "user_id": user_id,
                "artilheiro": artilheiro.strip(),
                "mvp": mvp.strip(),
                "goleiro": goleiro.strip(),
                "updated_at": now,
            },
            on_conflict="user_id",
        ).execute()
        return True
    except Exception:
        return False


def get_special_results() -> dict:
    client = get_admin_supabase()
    try:
        result = (
            client.table("special_results")
            .select("*")
            .eq("id", 1)
            .limit(1)
            .execute()
        )
        return result.data[0] if result.data else {}
    except Exception:
        return {}


# ── Ranking ───────────────────────────────────────────────────────────────────

def get_ranking() -> list[dict]:
    client = get_admin_supabase()
    profiles = client.table("profiles").select("id, nickname, department, shift").execute().data or []
    preds = client.table("predictions").select("user_id, points").execute().data or []
    specials = (
        client.table("special_predictions").select("user_id, points").execute().data or []
    )

    match_pts: dict[str, int] = {}
    for p in preds:
        match_pts[p["user_id"]] = match_pts.get(p["user_id"], 0) + (p["points"] or 0)

    special_pts: dict[str, int] = {s["user_id"]: (s["points"] or 0) for s in specials}

    ranking = []
    for prof in profiles:
        uid = prof["id"]
        mp = match_pts.get(uid, 0)
        sp = special_pts.get(uid, 0)
        ranking.append(
            {
                "nickname": prof["nickname"],
                "department": prof.get("department") or "—",
                "shift": prof.get("shift") or "—",
                "match_points": mp,
                "special_points": sp,
                "total_points": mp + sp,
            }
        )

    ranking.sort(key=lambda x: x["total_points"], reverse=True)
    return ranking


# ── Admin ─────────────────────────────────────────────────────────────────────

def update_match_result(match_id: int, result_a: int, result_b: int) -> bool:
    client = get_admin_supabase()
    try:
        client.table("matches").update(
            {"result_a": result_a, "result_b": result_b, "finished": True}
        ).eq("id", match_id).execute()
        _recalculate_match_points(match_id, result_a, result_b)
        return True
    except Exception:
        return False


def _recalculate_match_points(match_id: int, result_a: int, result_b: int) -> None:
    client = get_admin_supabase()
    preds = (
        client.table("predictions")
        .select("id, pred_a, pred_b")
        .eq("match_id", match_id)
        .execute()
        .data or []
    )
    for pred in preds:
        pts = calculate_match_points(pred["pred_a"], pred["pred_b"], result_a, result_b)
        client.table("predictions").update({"points": pts}).eq("id", pred["id"]).execute()


def recalculate_special_points() -> None:
    """Recalculate special points for all users based on current special_results."""
    client = get_admin_supabase()
    result_row = get_special_results()
    if not result_row:
        return
    specials = client.table("special_predictions").select("id, artilheiro, mvp, goleiro").execute().data or []
    for sp in specials:
        pts = calculate_special_points(sp, result_row)
        client.table("special_predictions").update({"points": pts}).eq("id", sp["id"]).execute()


def save_special_results(artilheiro: str, mvp: str, goleiro: str) -> bool:
    client = get_admin_supabase()
    now = datetime.now(timezone.utc).isoformat()
    try:
        client.table("special_results").upsert(
            {
                "id": 1,
                "artilheiro": artilheiro.strip(),
                "mvp": mvp.strip(),
                "goleiro": goleiro.strip(),
                "updated_at": now,
            }
        ).execute()
        recalculate_special_points()
        return True
    except Exception:
        return False


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


def reseed_matches() -> bool:
    """Delete all predictions and matches, then re-insert official fixtures."""
    from data.matches import get_all_fixtures

    client = get_admin_supabase()
    try:
        client.table("predictions").delete().neq("id", 0).execute()
        client.table("special_predictions").delete().neq("id", 0).execute()
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
