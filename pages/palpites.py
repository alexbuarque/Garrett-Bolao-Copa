from datetime import datetime, timezone, timedelta

BRASILIA = timezone(timedelta(hours=-3))

import streamlit as st

from utils.auth import is_logged_in
from utils.data import get_all_matches, get_user_predictions, save_prediction, get_playoff_matches
from utils.flags import with_flag_html
from data.matches import ALL_TEAMS, STAGE_LABELS, STAGE_ORDER

if not is_logged_in():
    st.warning("Faça login para dar seus palpites.")
    st.stop()

st.title("⚽ Palpites")

user_id = st.session_state["user_id"]
now = datetime.now(timezone.utc)
user_preds = get_user_predictions(user_id)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _render_match_card(match: dict, key_suffix: str) -> dict | None:
    """Renders one match card. Returns pending dict if bet is open, else None."""
    match_id = match["id"]
    match_dt = datetime.fromisoformat(match["match_date"])
    if match_dt.tzinfo is None:
        match_dt = match_dt.replace(tzinfo=timezone.utc)

    locked = now >= match_dt
    finished = match.get("finished", False)
    has_result = finished and match.get("result_a") is not None
    existing = user_preds.get(match_id)

    with st.container(border=True):
        col_info, col_preds = st.columns([2, 3])
        with col_info:
            ta_html = with_flag_html(match["team_a"])
            tb_html = with_flag_html(match["team_b"])
            st.markdown(f"<b>{ta_html}</b> vs <b>{tb_html}</b>", unsafe_allow_html=True)
            st.caption(match_dt.astimezone(BRASILIA).strftime("%d/%m/%Y %H:%M (Brasília)"))
            if has_result:
                st.markdown(f"✅ Resultado: **{match['result_a']} × {match['result_b']}**")
            elif locked:
                st.markdown("🔒 *Jogo em andamento / encerrado*")

        with col_preds:
            if has_result:
                if existing:
                    pts = existing.get("points", 0)
                    st.markdown(
                        f"Seu palpite: **{existing['pred_a']} × {existing['pred_b']}** "
                        f"→ **{pts} pt{'s' if pts != 1 else ''}**"
                    )
                else:
                    st.markdown("*Sem palpite registrado.*")
            elif locked:
                if existing:
                    st.markdown(f"Palpite salvo: **{existing['pred_a']} × {existing['pred_b']}** 🔒")
                else:
                    st.markdown("*Sem palpite — prazo encerrado.*")
            else:
                default_a = existing["pred_a"] if existing else 0
                default_b = existing["pred_b"] if existing else 0
                if existing:
                    st.caption(
                        f"✅ Palpite salvo: {existing['pred_a']} × {existing['pred_b']}"
                        " — altere abaixo e salve novamente se quiser"
                    )
                else:
                    st.caption("Sem palpite ainda — preencha e salve")
                c1, c2, c3 = st.columns([2, 1, 2])
                with c1:
                    ga = st.number_input(
                        match["team_a"], min_value=0, max_value=20,
                        value=int(default_a), key=f"ga_{key_suffix}_{match_id}",
                    )
                with c2:
                    st.markdown(
                        "<div style='text-align:center;padding-top:30px'>×</div>",
                        unsafe_allow_html=True,
                    )
                with c3:
                    gb = st.number_input(
                        match["team_b"], min_value=0, max_value=20,
                        value=int(default_b), key=f"gb_{key_suffix}_{match_id}",
                    )
                return {"match_id": match_id, "ga": ga, "gb": gb, "match_dt": match_dt}
    return None


def _save_pending(pending: list[dict], label: str, key: str) -> None:
    if not pending:
        return
    if st.button(f"💾 Salvar palpites — {label}", use_container_width=True, key=f"save_{key}"):
        saved = blocked = 0
        save_now = datetime.now(timezone.utc)
        for p in pending:
            if save_now < p["match_dt"]:
                if save_prediction(user_id, p["match_id"], p["ga"], p["gb"]):
                    saved += 1
            else:
                blocked += 1
        if saved:
            st.toast(f"Palpites salvos! ({saved} jogo(s))", icon="✅")
        if blocked:
            st.warning(f"{blocked} jogo(s) não foram salvos pois o prazo já encerrou.", icon="⚠️")
        st.rerun()


# ── Fase de Grupos ────────────────────────────────────────────────────────────

st.subheader("Fase de Grupos")

GROUPS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

all_matches = get_all_matches()
matches_by_group: dict[str, list] = {g: [] for g in GROUPS}
for m in all_matches:
    g = m.get("group_name")
    if g in matches_by_group:
        matches_by_group[g].append(m)

group_tabs = st.tabs([f"Grupo {g}" for g in GROUPS])
for tab, group in zip(group_tabs, GROUPS):
    with tab:
        matches = matches_by_group[group]
        if not matches:
            st.info("Nenhum jogo encontrado para este grupo.")
            continue
        pending = [r for m in matches if (r := _render_match_card(m, "g")) is not None]
        _save_pending(pending, f"Grupo {group}", f"group_{group}")

# ── Mata-mata ─────────────────────────────────────────────────────────────────

st.divider()
st.subheader("⚡ Mata-mata")

playoff_matches = get_playoff_matches()
confirmed = [m for m in playoff_matches if m["team_a"] in ALL_TEAMS and m["team_b"] in ALL_TEAMS]

if not confirmed:
    st.info(
        "Os confrontos do mata-mata ainda não foram definidos. "
        "Volte assim que a fase de grupos terminar! 🏆",
        icon="⏳",
    )
else:
    knockout_stages = [s for s in STAGE_ORDER if s != "group"]
    stages_with_matches = [
        (s, [m for m in confirmed if m["stage"] == s])
        for s in knockout_stages
        if any(m["stage"] == s for m in confirmed)
    ]

    playoff_tabs = st.tabs([STAGE_LABELS[s] for s, _ in stages_with_matches])
    for (stage_key, stage_matches), tab in zip(stages_with_matches, playoff_tabs):
        with tab:
            pending = [r for m in stage_matches if (r := _render_match_card(m, stage_key)) is not None]
            _save_pending(pending, STAGE_LABELS[stage_key], stage_key)
