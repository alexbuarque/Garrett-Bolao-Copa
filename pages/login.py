import streamlit as st
from utils.auth import is_logged_in, login, register, logout, reset_password, complete_password_reset

DEPARTMENTS = [
    "Engenharia", "Garantia", "IAM Vendas", "OE Vendas", "Financeiro", "Fiscal",
    "Desmontagem", "Montagem", "Manutenção", "Warehouse", "Yusen",
    "Indaiá", "Qualidade", "RH", "HSE", "IT", "Manufatura",
    "Produção", "NPI", "ISC", "Usinagem", "GEM", "PM", "Supply Chain", 
]

SHIFTS = ["1º Turno", "2º Turno", "3º Turno", "ADM"]

# ── Recovery mode (user clicked reset-password link in email) ─────────────────
params = st.query_params
if params.get("type") == "recovery":
    st.title("🔐 Redefinir Senha")
    token_hash = params.get("token_hash", "")
    if not token_hash:
        st.error("Link inválido ou expirado. Solicite um novo link de redefinição.")
        st.stop()
    with st.form("form_new_password"):
        new_pass = st.text_input("Nova senha (mínimo 6 caracteres)", type="password")
        new_pass2 = st.text_input("Confirmar nova senha", type="password")
        submitted_np = st.form_submit_button("Salvar nova senha", use_container_width=True)
    if submitted_np:
        if not new_pass or len(new_pass) < 6:
            st.error("A senha precisa ter ao menos 6 caracteres.")
        elif new_pass != new_pass2:
            st.error("As senhas não coincidem.")
        else:
            ok, err = complete_password_reset(token_hash, new_pass)
            if ok:
                st.success("Senha redefinida com sucesso! Faça login com a nova senha.")
                st.query_params.clear()
            else:
                st.error(err or "Erro ao redefinir senha. O link pode ter expirado.")
    st.stop()

# ── Normal login / register flow ──────────────────────────────────────────────
st.title("🔐 Bolão da Copa 2026")

if is_logged_in():
    st.success(f"Você está logado como **{st.session_state['nickname']}**.")
    if st.button("Sair"):
        logout()
        st.rerun()
    st.stop()

tab_login, tab_register, tab_reset = st.tabs(["Entrar", "Criar conta", "Esqueci a senha"])

# ── Login ─────────────────────────────────────────────────────────────────────
with tab_login:
    with st.form("form_login"):
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar", use_container_width=True)
    if submitted:
        if not email or not password:
            st.error("Preencha email e senha.")
        else:
            ok, err = login(email, password)
            if ok:
                st.session_state["redirect_to_palpites"] = True
                st.rerun()
            else:
                st.error(err or "Erro ao fazer login.")

# ── Criar conta ───────────────────────────────────────────────────────────────
with tab_register:
    with st.form("form_register"):
        r_email = st.text_input("Email", key="r_email")
        r_nick = st.text_input("Apelido (como aparecerá no ranking)")
        r_dept = st.selectbox("Departamento", DEPARTMENTS, key="r_dept")
        r_shift = st.selectbox("Turno", SHIFTS, key="r_shift")
        r_pass = st.text_input("Senha (mínimo 6 caracteres)", type="password", key="r_pass")
        r_pass2 = st.text_input("Confirmar senha", type="password", key="r_pass2")
        submitted_r = st.form_submit_button("Criar conta", use_container_width=True)
    if submitted_r:
        if not r_email or not r_nick or not r_pass:
            st.error("Preencha todos os campos.")
        elif r_pass != r_pass2:
            st.error("As senhas não coincidem.")
        elif len(r_pass) < 6:
            st.error("A senha precisa ter ao menos 6 caracteres.")
        else:
            ok, err = register(r_email, r_pass, r_nick, r_dept, r_shift)
            if ok:
                st.session_state["redirect_to_palpites"] = True
                st.rerun()
            else:
                st.error(err or "Erro ao criar conta.")

# ── Esqueci a senha ───────────────────────────────────────────────────────────
with tab_reset:
    st.markdown(
        "Informe o email cadastrado e enviaremos um link para você criar uma nova senha."
    )
    with st.form("form_reset"):
        reset_email = st.text_input("Email cadastrado", key="reset_email")
        submitted_reset = st.form_submit_button(
            "Enviar link de redefinição", use_container_width=True
        )
    if submitted_reset:
        if not reset_email:
            st.error("Informe seu email.")
        else:
            ok, err = reset_password(reset_email)
            if ok:
                st.success(
                    "Link enviado! Verifique sua caixa de entrada (e a pasta de spam) "
                    "e siga as instruções para criar uma nova senha."
                )
            else:
                st.error(err or "Erro ao enviar o email de redefinição.")
