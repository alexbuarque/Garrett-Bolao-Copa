import pandas as pd
import streamlit as st

from utils.auth import is_logged_in
from utils.data import get_ranking

st.title("🏆 Ranking")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div style="background-color:#FFD700;border-radius:12px;padding:20px;text-align:center;margin-bottom:12px">
            <div style="font-size:2rem">🥇</div>
            <div style="font-size:1rem;font-weight:bold;color:#333">1º Lugar</div>
            <div style="font-size:1rem;color:#333;margin-top:6px">🎁 Vale Presente</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div style="background-color:#C0C0C0;border-radius:12px;padding:20px;text-align:center;margin-bottom:12px">
            <div style="font-size:2rem">🥈</div>
            <div style="font-size:1rem;font-weight:bold;color:#333">2º Lugar</div>
            <div style="font-size:1rem;color:#333;margin-top:6px">🎁 Vale Presente</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div style="background-color:#CD7F32;border-radius:12px;padding:20px;text-align:center;margin-bottom:12px">
            <div style="font-size:2rem">🥉</div>
            <div style="font-size:1rem;font-weight:bold;color:#333">3º Lugar</div>
            <div style="font-size:1rem;color:#333;margin-top:6px">🎁 Vale Presente</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

ranking = get_ranking()

if not ranking:
    st.info("Nenhum participante cadastrado ainda. Seja o primeiro! 🎉")
    st.stop()

current_nickname = st.session_state.get("nickname") if is_logged_in() else None

rows = []
for pos, entry in enumerate(ranking, start=1):
    medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(pos, str(pos))
    rows.append(
        {
            "Pos.": medal,
            "Participante": entry["nickname"],
            "Departamento": entry["department"],
            "Turno": entry["shift"],
            "Pontos": entry["total_points"],
        }
    )

df = pd.DataFrame(rows)

def highlight_user(row):
    if row["Participante"] == current_nickname:
        return ["background-color: #1a472a; color: white"] * len(row)
    return [""] * len(row)

styled = df.style.apply(highlight_user, axis=1)

st.dataframe(
    styled,
    use_container_width=True,
    hide_index=True,
)

st.caption("Pontuação: Placar exato = 5 pts | Vencedor/empate = 3 pts")
