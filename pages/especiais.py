from datetime import datetime, timezone

import streamlit as st

from data.matches import TOURNAMENT_START
from utils.auth import is_logged_in
from utils.data import get_special_prediction, get_special_results, save_special_prediction

if not is_logged_in():
    st.warning("Faça login para dar seus palpites especiais.")
    st.stop()

st.title("🌟 Palpites Especiais")

user_id = st.session_state["user_id"]
now = datetime.now(timezone.utc)
locked = now >= TOURNAMENT_START

existing = get_special_prediction(user_id) or {}
results = get_special_results()

st.markdown(
    """
    Dê seus palpites para os prêmios individuais da Copa.
    Cada acerto vale **10 pontos**!
    """
)

if locked:
    st.warning("🔒 O torneio já começou — palpites especiais não podem mais ser alterados.")

with st.form("form_especiais"):
    artilheiro = st.text_input(
        "⚽ Artilheiro da Copa (jogador que vai fazer mais gols)",
        value=existing.get("artilheiro", ""),
        disabled=locked,
        placeholder="Nome do jogador",
    )
    mvp = st.text_input(
        "🏅 MVP da Copa (melhor jogador do torneio)",
        value=existing.get("mvp", ""),
        disabled=locked,
        placeholder="Nome do jogador",
    )
    goleiro = st.text_input(
        "🧤 Melhor Goleiro da Copa",
        value=existing.get("goleiro", ""),
        disabled=locked,
        placeholder="Nome do goleiro",
    )
    submit = st.form_submit_button("💾 Salvar palpites especiais", disabled=locked, use_container_width=True)

if submit and not locked:
    if save_special_prediction(user_id, artilheiro, mvp, goleiro):
        st.success("✅ Palpites especiais salvos!")
        st.rerun()
    else:
        st.error("Erro ao salvar palpites. Tente novamente.")

# ── Show current prediction summary ──
if existing:
    st.divider()
    st.subheader("📋 Seus palpites registrados")
    col1, col2, col3 = st.columns(3)
    col1.metric("⚽ Artilheiro", existing.get("artilheiro") or "—")
    col2.metric("🏅 MVP", existing.get("mvp") or "—")
    col3.metric("🧤 Melhor Goleiro", existing.get("goleiro") or "—")
    pts = existing.get("points", 0)
    if pts > 0:
        st.success(f"Você marcou **{pts} ponto(s)** nos especiais.")

# ── Show revealed results ──
if results and any(results.get(k) for k in ("artilheiro", "mvp", "goleiro")):
    st.divider()
    st.subheader("🏆 Resultados oficiais revelados")
    col1, col2, col3 = st.columns(3)
    col1.metric("⚽ Artilheiro", results.get("artilheiro") or "—")
    col2.metric("🏅 MVP", results.get("mvp") or "—")
    col3.metric("🧤 Melhor Goleiro", results.get("goleiro") or "—")
