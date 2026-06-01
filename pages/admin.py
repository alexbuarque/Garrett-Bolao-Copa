from datetime import datetime, timezone, timedelta

BRASILIA = timezone(timedelta(hours=-3))

import pandas as pd
import streamlit as st

from utils.data import (
    get_all_matches,
    get_predictions_for_match,
    get_special_results,
    save_special_results,
    update_match_result,
    seed_matches_if_empty,
    reseed_matches,
)

st.title("🔧 Painel Administrativo")

# ── Password gate — only st.stop() at page level is safe ─────────────────────
if "admin_authed" not in st.session_state:
    st.session_state["admin_authed"] = False

if not st.session_state["admin_authed"]:
    with st.form("admin_login"):
        pwd = st.text_input("Senha do administrador", type="password")
        ok = st.form_submit_button("Entrar")
    if ok:
        try:
            correct = st.secrets["ADMIN_PASSWORD"]
        except Exception:
            correct = ""
        if pwd == correct:
            st.session_state["admin_authed"] = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
    st.stop()

st.success("✅ Acesso administrativo ativo.")

# Fetch matches once, share across tabs
all_matches = get_all_matches()

tab_seed, tab_results, tab_especiais, tab_view = st.tabs(
    ["⚙️ Inicializar", "📋 Resultados", "🌟 Especiais", "👁️ Ver Palpites"]
)

# ── Seed ──────────────────────────────────────────────────────────────────────
with tab_seed:
    st.markdown(
        "Se a tabela `matches` estiver vazia, clique abaixo para inserir todos os 72 jogos."
    )
    if st.button("Inicializar jogos no banco de dados", use_container_width=True):
        seed_matches_if_empty()
        st.success("Jogos verificados/inseridos com sucesso!")

    st.divider()
    st.subheader("⚠️ Recriar jogos oficiais")
    st.warning(
        "Esta ação **apaga todos os palpites e jogos existentes** e reinserirá "
        "os 72 jogos oficiais da Copa 2026. Use somente se os jogos estiverem incorretos."
    )
    confirm_reseed = st.checkbox(
        "Confirmo que entendo que todos os palpites serão perdidos"
    )
    if st.button(
        "🔄 Recriar jogos oficiais",
        use_container_width=True,
        disabled=not confirm_reseed,
    ):
        if reseed_matches():
            st.success("Jogos recriados com sucesso! Todos os palpites foram removidos.")
            st.rerun()
        else:
            st.error("Erro ao recriar jogos.")

# ── Match Results ─────────────────────────────────────────────────────────────
with tab_results:
    st.subheader("Registrar resultado de jogo")
    if not all_matches:
        st.warning("Nenhum jogo encontrado. Use a aba ⚙️ Inicializar primeiro.")
    else:
        GROUPS = sorted({m["group_name"] for m in all_matches})
        group_sel = st.selectbox("Grupo", GROUPS, key="admin_group")
        group_matches = [m for m in all_matches if m["group_name"] == group_sel]

        for match in group_matches:
            match_id = match["id"]
            finished = match.get("finished", False)
            status = "✅" if finished else "⏳"
            label = (
                f"{status} {match['team_a']} × {match['team_b']} "
                f"({datetime.fromisoformat(match['match_date']).astimezone(BRASILIA).strftime('%d/%m %H:%M')} BRT)"
            )
            with st.expander(label, expanded=not finished):
                with st.form(f"form_result_{match_id}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        r_a = st.number_input(
                            f"Gols {match['team_a']}",
                            min_value=0,
                            max_value=30,
                            value=int(match.get("result_a") or 0),
                            key=f"ra_{match_id}",
                        )
                    with col2:
                        r_b = st.number_input(
                            f"Gols {match['team_b']}",
                            min_value=0,
                            max_value=30,
                            value=int(match.get("result_b") or 0),
                            key=f"rb_{match_id}",
                        )
                    save_btn = st.form_submit_button(
                        "💾 Salvar resultado e calcular pontos",
                        use_container_width=True,
                    )
                if save_btn:
                    if update_match_result(match_id, r_a, r_b):
                        st.success(f"Resultado salvo: {r_a} × {r_b}. Pontos recalculados!")
                        st.rerun()
                    else:
                        st.error("Erro ao salvar resultado.")

# ── Special Results ───────────────────────────────────────────────────────────
with tab_especiais:
    st.subheader("Revelar prêmios especiais")
    current = get_special_results()
    with st.form("form_special_results"):
        art = st.text_input("⚽ Artilheiro", value=current.get("artilheiro") or "")
        mvp_val = st.text_input("🏅 MVP", value=current.get("mvp") or "")
        gol = st.text_input("🧤 Melhor Goleiro", value=current.get("goleiro") or "")
        save_sp = st.form_submit_button(
            "💾 Salvar e recalcular pontos especiais", use_container_width=True
        )
    if save_sp:
        if save_special_results(art, mvp_val, gol):
            st.success("Resultados especiais salvos e pontos recalculados!")
        else:
            st.error("Erro ao salvar.")

# ── View Predictions ──────────────────────────────────────────────────────────
with tab_view:
    st.subheader("Ver palpites de um jogo")
    if not all_matches:
        st.warning("Nenhum jogo cadastrado.")
    else:
        options = {
            f"{m['team_a']} × {m['team_b']} (Grupo {m['group_name']})": m["id"]
            for m in all_matches
        }
        selected_label = st.selectbox("Selecione o jogo", list(options.keys()))
        selected_id = options[selected_label]

        if st.button("🔍 Ver palpites", use_container_width=True):
            preds = get_predictions_for_match(selected_id)
            if not preds:
                st.info("Nenhum palpite registrado para este jogo.")
            else:
                df = pd.DataFrame(preds).rename(
                    columns={
                        "nickname": "Participante",
                        "pred_a": "Time A",
                        "pred_b": "Time B",
                        "points": "Pontos",
                    }
                )
                df = df.sort_values("Pontos", ascending=False)
                st.dataframe(df, use_container_width=True, hide_index=True)
