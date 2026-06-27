from datetime import datetime, timedelta, timezone

import pandas as pd
import streamlit as st

from utils.data import get_all_matches, get_all_predictions_with_profiles
from utils.flags import with_flag_html

BRASILIA = timezone(timedelta(hours=-3))

st.title("🔍 Palpites de Todos")

matches = get_all_matches()
if not matches:
    st.info("Nenhum jogo cadastrado ainda.")
    st.stop()

all_preds = get_all_predictions_with_profiles()

groups = sorted({m["group_name"] for m in matches})
tabs = st.tabs([f"Grupo {g}" for g in groups])

for tab, group in zip(tabs, groups):
    with tab:
        group_matches = [m for m in matches if m["group_name"] == group]
        for match in group_matches:
            mid = match["id"]
            finished = match.get("finished", False)
            dt = datetime.fromisoformat(match["match_date"]).astimezone(BRASILIA)

            # Expander label (plain text — HTML not supported here)
            if finished:
                label = (
                    f"✅ {match['team_a']} {match['result_a']} × {match['result_b']} "
                    f"{match['team_b']} — {dt.strftime('%d/%m %H:%M')} BRT"
                )
            else:
                label = f"⏳ {match['team_a']} × {match['team_b']} — {dt.strftime('%d/%m %H:%M')} BRT"

            preds = all_preds.get(mid, [])
            with st.expander(label, expanded=False):
                # Match header with flag images (HTML works inside expander body)
                ta_html = with_flag_html(match["team_a"])
                tb_html = with_flag_html(match["team_b"])
                if finished:
                    st.markdown(
                        f"<b>{ta_html} {match['result_a']} × {match['result_b']} {tb_html}</b>"
                        f" &nbsp;·&nbsp; {dt.strftime('%d/%m/%Y %H:%M')} (Brasília)",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<b>{ta_html}</b> vs <b>{tb_html}</b>"
                        f" &nbsp;·&nbsp; {dt.strftime('%d/%m/%Y %H:%M')} (Brasília)",
                        unsafe_allow_html=True,
                    )

                if not preds:
                    st.caption("Nenhum palpite registrado.")
                else:
                    rows = []
                    for p in sorted(preds, key=lambda x: x["nickname"].lower()):
                        palpite = f"{p['pred_a']} × {p['pred_b']}"
                        if p.get("pred_penalties") and p.get("pred_pen_a") is not None:
                            palpite += f" (pên: {p['pred_pen_a']} × {p['pred_pen_b']})"
                        rows.append({
                            "Participante": p["nickname"],
                            "Palpite": palpite,
                            "Pts": p["points"] if finished else "—",
                        })
                    df = pd.DataFrame(rows)
                    st.dataframe(df, use_container_width=True, hide_index=True)
