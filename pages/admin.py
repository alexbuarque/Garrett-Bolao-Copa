from datetime import datetime, timezone, timedelta

BRASILIA = timezone(timedelta(hours=-3))

import pandas as pd
import streamlit as st

from utils.data import (
    get_all_matches,
    get_predictions_for_match,
    update_match_result,
    seed_matches_if_empty,
    reseed_matches,
    get_orphaned_predictions,
    create_missing_profile,
    seed_playoffs_if_empty,
    get_playoff_matches,
    update_match_teams,
    update_match_datetime,
)
from data.matches import STAGE_LABELS, STAGE_ORDER
from utils.supabase_client import get_admin_supabase

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

DEPARTMENTS = [
    "Engenharia", "Garantia", "IAM Vendas", "OE Vendas", "Financeiro", "Fiscal",
    "Desmontagem", "Montagem", "Manutenção", "Warehouse", "Yusen",
    "Indaiá", "Qualidade", "RH", "HSE", "IT", "Manufatura",
    "Produção", "NPI", "ISC", "Usinagem", "GEM", "PM", "Supply Chain", "Supply Base",
]
SHIFTS = ["1º Turno", "2º Turno", "3º Turno", "ADM"]

tab_seed, tab_results, tab_playoffs, tab_view, tab_diag = st.tabs(
    ["⚙️ Inicializar", "📋 Resultados", "🏆 Playoffs", "👁️ Ver Palpites", "🔍 Diagnóstico"]
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

# ── Playoffs ──────────────────────────────────────────────────────────────────
with tab_playoffs:
    st.subheader("Inicializar jogos eliminatórios")
    st.markdown(
        "Insere os 32 jogos do mata-mata com times placeholder. "
        "Após confirmar os classificados, edite os times em cada jogo abaixo."
    )
    if st.button("➕ Inserir jogos eliminatórios", use_container_width=True):
        ok, count = seed_playoffs_if_empty()
        if ok:
            st.success(f"{count} jogos inseridos com sucesso!")
            st.rerun()
        else:
            st.info("Os jogos eliminatórios já estão cadastrados.")

    st.divider()

    playoff_matches = get_playoff_matches()
    if not playoff_matches:
        st.info("Nenhum jogo eliminatório cadastrado. Use o botão acima para inserir.")
    else:
        knockout_stages = [s for s in STAGE_ORDER if s != "group"]
        for stage_key in knockout_stages:
            stage_matches = [m for m in playoff_matches if m.get("stage") == stage_key]
            if not stage_matches:
                continue
            st.subheader(STAGE_LABELS[stage_key])
            for match in stage_matches:
                mid = match["id"]
                match_dt = datetime.fromisoformat(match["match_date"])
                if match_dt.tzinfo is None:
                    match_dt = match_dt.replace(tzinfo=timezone.utc)
                match_dt_brt = match_dt.astimezone(BRASILIA)
                finished = match.get("finished", False)
                status = "✅" if finished else "⏳"
                label = (
                    f"{status} {match['team_a']} × {match['team_b']} "
                    f"— {match_dt_brt.strftime('%d/%m %H:%M')} BRT"
                )
                with st.expander(label, expanded=False):
                    col_teams, col_dt = st.columns(2)

                    with col_teams:
                        st.markdown("**Atualizar times**")
                        with st.form(f"teams_{mid}"):
                            new_a = st.text_input("Time A", value=match["team_a"], key=f"ta_{mid}")
                            new_b = st.text_input("Time B", value=match["team_b"], key=f"tb_{mid}")
                            if st.form_submit_button("💾 Salvar times", use_container_width=True):
                                if update_match_teams(mid, new_a, new_b):
                                    st.success("Times atualizados!")
                                    st.rerun()
                                else:
                                    st.error("Erro ao salvar.")

                    with col_dt:
                        st.markdown("**Atualizar horário (Brasília)**")
                        with st.form(f"dt_{mid}"):
                            new_date = st.date_input("Data", value=match_dt_brt.date(), key=f"d_{mid}")
                            new_time = st.time_input("Hora", value=match_dt_brt.time(), key=f"t_{mid}")
                            if st.form_submit_button("💾 Salvar horário", use_container_width=True):
                                from datetime import datetime as dt
                                brt_dt = dt.combine(new_date, new_time).replace(tzinfo=BRASILIA)
                                utc_iso = brt_dt.astimezone(timezone.utc).isoformat()
                                if update_match_datetime(mid, utc_iso):
                                    st.success("Horário atualizado!")
                                    st.rerun()
                                else:
                                    st.error("Erro ao salvar.")

                    if finished:
                        st.markdown(
                            f"✅ Resultado registrado: **{match['result_a']} × {match['result_b']}**"
                        )
                    else:
                        st.caption("Resultado ainda não registrado — use a aba 📋 Resultados.")

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

# ── Diagnóstico ───────────────────────────────────────────────────────────────
with tab_diag:
    st.subheader("Usuários com palpites sem perfil")
    st.markdown(
        "Identifica usuários que possuem palpites registrados mas não têm perfil na "
        "tabela de participantes — esses usuários não aparecem no ranking nem em "
        "Palpites de Todos."
    )

    orphans = get_orphaned_predictions()

    if not orphans:
        st.success("✅ Nenhum problema encontrado. Todos os palpites têm perfil correspondente.")
    else:
        st.warning(f"⚠️ {len(orphans)} usuário(s) com palpites mas sem perfil cadastrado.")

        # Try to fetch emails from Supabase Auth
        try:
            auth_users = get_admin_supabase().auth.admin.list_users()
            auth_map = {u.id: u.email for u in auth_users}
        except Exception:
            auth_map = {}

        for orphan in orphans:
            uid = orphan["user_id"]
            email = auth_map.get(uid, "email não encontrado")
            label = f"{email} — {orphan['pred_count']} palpite(s), {orphan['total_points']} pts"
            with st.expander(f"⚠️ {label}"):
                st.caption(f"user_id: `{uid}`")
                with st.form(f"fix_{uid}"):
                    default_nick = email.split("@")[0] if "@" in email else ""
                    fix_nick = st.text_input("Apelido", value=default_nick, key=f"nick_{uid}")
                    fix_dept = st.selectbox("Departamento", [""] + DEPARTMENTS, key=f"dept_{uid}")
                    fix_shift = st.selectbox("Turno", [""] + SHIFTS, key=f"shift_{uid}")
                    fix_btn = st.form_submit_button("Criar perfil para este usuário", use_container_width=True)
                if fix_btn:
                    if not fix_nick.strip():
                        st.error("Informe um apelido.")
                    elif create_missing_profile(uid, fix_nick, fix_dept, fix_shift):
                        st.success(f"Perfil criado para **{fix_nick}**! Os palpites já aparecem no ranking.")
                        st.rerun()
                    else:
                        st.error("Erro ao criar perfil. O apelido pode já estar em uso.")
