from datetime import datetime, timezone, timedelta

BRASILIA = timezone(timedelta(hours=-3))

import streamlit as st

from utils.auth import is_logged_in
from utils.data import get_user_predictions, save_prediction, get_playoff_matches
from utils.flags import with_flag_html
from data.matches import ALL_TEAMS, STAGE_LABELS, STAGE_ORDER

if not is_logged_in():
    st.warning("Faça login para dar seus palpites.")
    st.stop()

st.title("⚡ Palpites — Mata-mata")

user_id = st.session_state["user_id"]
now = datetime.now(timezone.utc)
user_preds = get_user_predictions(user_id)


def _render_match_card(match: dict) -> dict | None:
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
                res_line = f"✅ Resultado: **{match['result_a']} × {match['result_b']}**"
                if match.get("result_penalties"):
                    res_line += (
                        f" *(pênaltis: {match['result_pen_a']} × {match['result_pen_b']})*"
                    )
                st.markdown(res_line)
            elif locked:
                st.markdown("🔒 *Jogo em andamento / encerrado*")

        with col_preds:
            if has_result:
                if existing:
                    pts = existing.get("points", 0)
                    pred_line = (
                        f"Seu palpite: **{existing['pred_a']} × {existing['pred_b']}**"
                    )
                    if existing.get("pred_penalties") and existing.get("pred_pen_a") is not None:
                        pred_line += (
                            f" *(pênaltis: {existing['pred_pen_a']} × {existing['pred_pen_b']})*"
                        )
                    pred_line += f" → **{pts} pt{'s' if pts != 1 else ''}**"
                    st.markdown(pred_line)
                else:
                    st.markdown("*Sem palpite registrado.*")

            elif locked:
                if existing:
                    pred_line = (
                        f"Palpite salvo: **{existing['pred_a']} × {existing['pred_b']}**"
                    )
                    if existing.get("pred_penalties") and existing.get("pred_pen_a") is not None:
                        pred_line += (
                            f" *(pênaltis: {existing['pred_pen_a']} × {existing['pred_pen_b']})*"
                        )
                    pred_line += " 🔒"
                    st.markdown(pred_line)
                else:
                    st.markdown("*Sem palpite — prazo encerrado.*")

            else:
                default_a = existing["pred_a"] if existing else 0
                default_b = existing["pred_b"] if existing else 0
                default_pen = bool(existing.get("pred_penalties")) if existing else False
                default_pen_a = existing.get("pred_pen_a") or 0 if existing else 0
                default_pen_b = existing.get("pred_pen_b") or 0 if existing else 0

                if existing:
                    saved_line = (
                        f"✅ Palpite salvo: {existing['pred_a']} × {existing['pred_b']}"
                    )
                    if existing.get("pred_penalties") and existing.get("pred_pen_a") is not None:
                        saved_line += (
                            f" | pênaltis: {existing['pred_pen_a']} × {existing['pred_pen_b']}"
                        )
                    saved_line += " — altere abaixo e salve novamente se quiser"
                    st.caption(saved_line)
                else:
                    st.caption("Sem palpite ainda — preencha e salve")

                # Score inputs
                c1, c2, c3 = st.columns([2, 1, 2])
                with c1:
                    ga = st.number_input(
                        match["team_a"], min_value=0, max_value=20,
                        value=int(default_a), key=f"ga_{match_id}",
                    )
                with c2:
                    st.markdown(
                        "<div style='text-align:center;padding-top:30px'>×</div>",
                        unsafe_allow_html=True,
                    )
                with c3:
                    gb = st.number_input(
                        match["team_b"], min_value=0, max_value=20,
                        value=int(default_b), key=f"gb_{match_id}",
                    )

                # Penalty shootout option
                goes_to_pen = st.checkbox(
                    "🥅 Vai para pênaltis?",
                    value=default_pen,
                    key=f"pen_{match_id}",
                )
                pen_a = pen_b = None
                if goes_to_pen:
                    st.caption(
                        "Informe o placar dos pênaltis "
                        "(o placar acima deve terminar empatado para ir a pênaltis)"
                    )
                    p1, p2, p3 = st.columns([2, 1, 2])
                    with p1:
                        pen_a = st.number_input(
                            f"Pênaltis {match['team_a']}", min_value=0, max_value=20,
                            value=int(default_pen_a), key=f"pena_{match_id}",
                        )
                    with p2:
                        st.markdown(
                            "<div style='text-align:center;padding-top:30px'>×</div>",
                            unsafe_allow_html=True,
                        )
                    with p3:
                        pen_b = st.number_input(
                            f"Pênaltis {match['team_b']}", min_value=0, max_value=20,
                            value=int(default_pen_b), key=f"penb_{match_id}",
                        )

                return {
                    "match_id": match_id,
                    "ga": ga, "gb": gb,
                    "match_dt": match_dt,
                    "pred_penalties": goes_to_pen,
                    "pred_pen_a": pen_a,
                    "pred_pen_b": pen_b,
                }
    return None


playoff_matches = get_playoff_matches()
confirmed = [m for m in playoff_matches if m["team_a"] in ALL_TEAMS and m["team_b"] in ALL_TEAMS]

if not confirmed:
    st.info(
        "Os confrontos do mata-mata ainda não foram definidos. "
        "Volte assim que a fase de grupos terminar! 🏆",
        icon="⏳",
    )
    st.stop()

knockout_stages = [s for s in STAGE_ORDER if s != "group"]
stages_with_matches = [
    (s, [m for m in confirmed if m["stage"] == s])
    for s in knockout_stages
    if any(m["stage"] == s for m in confirmed)
]

playoff_tabs = st.tabs([STAGE_LABELS[s] for s, _ in stages_with_matches])
for (stage_key, stage_matches), tab in zip(stages_with_matches, playoff_tabs):
    with tab:
        pending = [r for m in stage_matches if (r := _render_match_card(m)) is not None]

        if pending:
            if st.button(
                f"💾 Salvar palpites — {STAGE_LABELS[stage_key]}",
                use_container_width=True,
                key=f"save_{stage_key}",
            ):
                saved = blocked = 0
                save_now = datetime.now(timezone.utc)
                for p in pending:
                    if save_now < p["match_dt"]:
                        if save_prediction(
                            user_id, p["match_id"], p["ga"], p["gb"],
                            pred_penalties=p["pred_penalties"],
                            pred_pen_a=p["pred_pen_a"],
                            pred_pen_b=p["pred_pen_b"],
                        ):
                            saved += 1
                    else:
                        blocked += 1
                if saved:
                    st.toast(f"Palpites salvos! ({saved} jogo(s))", icon="✅")
                if blocked:
                    st.warning(
                        f"{blocked} jogo(s) não foram salvos pois o prazo já encerrou.",
                        icon="⚠️",
                    )
                st.rerun()
