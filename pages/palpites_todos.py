from datetime import datetime, timedelta, timezone

import pandas as pd
import streamlit as st

from utils.data import get_all_matches, get_all_predictions_with_profiles

BRASILIA = timezone(timedelta(hours=-3))

st.image("assets/banner.png", use_container_width=True)
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

            if finished:
                label = (
                    f"✅ {match['team_a']} {match['result_a']} × {match['result_b']} "
                    f"{match['team_b']} — {dt.strftime('%d/%m %H:%M')} BRT"
                )
            else:
                label = (
                    f"⏳ {match['team_a']} × {match['team_b']} "
                    f"— {dt.strftime('%d/%m %H:%M')} BRT"
                )

            preds = all_preds.get(mid, [])
            with st.expander(label, expanded=False):
                if not preds:
                    st.caption("Nenhum palpite registrado.")
                else:
                    rows = []
                    for p in sorted(preds, key=lambda x: x["nickname"].lower()):
                        rows.append({
                            "Participante": p["nickname"],
                            "Palpite": f"{p['pred_a']} × {p['pred_b']}",
                            "Pts": p["points"] if finished else "—",
                        })
                    df = pd.DataFrame(rows)
                    st.dataframe(df, use_container_width=True, hide_index=True)
