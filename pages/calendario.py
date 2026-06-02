from datetime import datetime, timedelta, timezone
from collections import defaultdict

import streamlit as st

from utils.data import get_all_matches
from utils.flags import with_flag_html

BRASILIA = timezone(timedelta(hours=-3))

DAYS_PT = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
MONTHS_PT = [
    "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]

st.title("📅 Calendário dos Jogos")

matches = get_all_matches()
if not matches:
    st.info("Nenhum jogo cadastrado ainda.")
    st.stop()

# ── Filters ───────────────────────────────────────────────────────────────────
all_groups = sorted({m["group_name"] for m in matches})
col_f1, col_f2 = st.columns([2, 3])
with col_f1:
    group_filter = st.selectbox(
        "Filtrar por grupo",
        ["Todos"] + [f"Grupo {g}" for g in all_groups],
    )

filtered = matches
if group_filter != "Todos":
    g = group_filter.replace("Grupo ", "")
    filtered = [m for m in matches if m["group_name"] == g]

# ── Group by date (BRT) ───────────────────────────────────────────────────────
by_date: dict[str, list] = defaultdict(list)
for m in filtered:
    dt_brt = datetime.fromisoformat(m["match_date"]).astimezone(BRASILIA)
    day_key = dt_brt.strftime("%Y-%m-%d")
    by_date[day_key].append((dt_brt, m))

now_brt = datetime.now(BRASILIA)

# ── Render ────────────────────────────────────────────────────────────────────
for day_key in sorted(by_date.keys()):
    day_matches = sorted(by_date[day_key], key=lambda x: x[0])
    dt_sample = day_matches[0][0]

    weekday = DAYS_PT[dt_sample.weekday()]
    month = MONTHS_PT[dt_sample.month]
    day_label = f"{weekday}, {dt_sample.day} de {month} de {dt_sample.year}"

    st.markdown(f"### 📆 {day_label}")

    cols = st.columns(2)
    for i, (dt_brt, match) in enumerate(day_matches):
        finished = match.get("finished", False)
        started = now_brt >= dt_brt

        if finished:
            status_color = "#1a472a"
            status_icon = "✅"
            status_text = f"{match['result_a']} × {match['result_b']}"
        elif started:
            status_color = "#7b3f00"
            status_icon = "🔴"
            status_text = "Em andamento"
        else:
            status_color = "#1a3a5c"
            status_icon = "🕐"
            status_text = dt_brt.strftime("%H:%M") + " (Brasília)"

        ta = with_flag_html(match["team_a"])
        tb = with_flag_html(match["team_b"])

        with cols[i % 2]:
            st.markdown(
                f"""
                <div style="
                    background-color:{status_color};
                    border-radius:10px;
                    padding:14px 18px;
                    margin-bottom:12px;
                ">
                    <div style="font-size:0.75rem;color:#ccc;margin-bottom:6px">
                        {status_icon} {status_text} &nbsp;·&nbsp; Grupo {match['group_name']}
                    </div>
                    <div style="font-size:1rem;font-weight:bold;color:#fff">
                        {ta} &nbsp;×&nbsp; {tb}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()
