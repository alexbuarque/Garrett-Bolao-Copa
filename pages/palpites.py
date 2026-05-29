from datetime import datetime, timezone

import streamlit as st

from utils.auth import is_logged_in
from utils.data import get_all_matches, get_user_predictions, save_prediction

if not is_logged_in():
    st.warning("Faça login para dar seus palpites.")
    st.stop()

st.title("⚽ Palpites — Fase de Grupos")

user_id = st.session_state["user_id"]
now = datetime.now(timezone.utc)

GROUPS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

# Single DB round-trip for all matches and user predictions
all_matches = get_all_matches()
user_preds = get_user_predictions(user_id)

# Group matches by group name
matches_by_group: dict[str, list] = {g: [] for g in GROUPS}
for m in all_matches:
    g = m.get("group_name")
    if g in matches_by_group:
        matches_by_group[g].append(m)

tabs = st.tabs([f"Grupo {g}" for g in GROUPS])

for tab, group in zip(tabs, GROUPS):
    with tab:
        matches = matches_by_group[group]
        if not matches:
            st.info("Nenhum jogo encontrado para este grupo.")
            continue

        pending: list[dict] = []

        for match in matches:
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
                    st.markdown(f"**{match['team_a']}** vs **{match['team_b']}**")
                    st.caption(match_dt.strftime("%d/%m/%Y %H:%M UTC"))
                    if has_result:
                        st.markdown(
                            f"✅ Resultado: **{match['result_a']} × {match['result_b']}**"
                        )
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
                            st.markdown(
                                f"Palpite salvo: **{existing['pred_a']} × {existing['pred_b']}** 🔒"
                            )
                        else:
                            st.markdown("*Sem palpite — prazo encerrado.*")
                    else:
                        default_a = existing["pred_a"] if existing else 0
                        default_b = existing["pred_b"] if existing else 0
                        c1, c2, c3 = st.columns([2, 1, 2])
                        with c1:
                            ga = st.number_input(
                                match["team_a"],
                                min_value=0,
                                max_value=20,
                                value=int(default_a),
                                key=f"ga_{match_id}",
                            )
                        with c2:
                            st.markdown(
                                "<div style='text-align:center;padding-top:30px'>×</div>",
                                unsafe_allow_html=True,
                            )
                        with c3:
                            gb = st.number_input(
                                match["team_b"],
                                min_value=0,
                                max_value=20,
                                value=int(default_b),
                                key=f"gb_{match_id}",
                            )
                        pending.append({"match_id": match_id, "ga": ga, "gb": gb, "match_dt": match_dt})

        if pending:
            if st.button(f"💾 Salvar palpites do Grupo {group}", use_container_width=True, key=f"save_{group}"):
                saved = 0
                save_now = datetime.now(timezone.utc)  # fresh timestamp at click time
                for p in pending:
                    if save_now < p["match_dt"]:
                        if save_prediction(user_id, p["match_id"], p["ga"], p["gb"]):
                            saved += 1
                st.success(f"✅ {saved} palpite(s) salvo(s) no Grupo {group}!")
                st.rerun()
