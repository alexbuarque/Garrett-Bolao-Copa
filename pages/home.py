import streamlit as st
from utils.auth import complete_password_reset

# Handle password recovery links that land on the home page (/?type=recovery&token_hash=...)
if st.query_params.get("type") == "recovery":
    token_hash = st.query_params.get("token_hash", "")
    st.title("🔐 Redefinir Senha")
    if not token_hash:
        st.error("Link inválido ou expirado. Solicite um novo link de redefinição.")
        st.stop()
    with st.form("form_new_password_home"):
        new_pass = st.text_input("Nova senha (mínimo 6 caracteres)", type="password")
        new_pass2 = st.text_input("Confirmar nova senha", type="password")
        submitted = st.form_submit_button("Salvar nova senha", use_container_width=True)
    if submitted:
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

st.markdown("## Ação entre amigos — Copa 2026")
st.markdown(
    "Bem-vindo à ação entre amigos da Copa do Mundo 2026! "
    "Esta iniciativa é destinada a **Colaboradores Garrett** e **Terceiros** "
    "que queiram participar de uma disputa amigável de palpites ao longo do torneio."
)

st.divider()

st.image("assets/banner.png", use_container_width=True)

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div style="background-color:#1a3a5c;border-radius:10px;padding:20px;text-align:center;margin-bottom:12px">
            <div style="font-size:2rem">⚽</div>
            <div style="font-size:1rem;font-weight:bold;color:#fff;margin-top:8px">Dê seus palpites</div>
            <div style="font-size:0.85rem;color:#ccc;margin-top:6px">
                Palpite nos jogos da fase de grupos antes de cada partida começar.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div style="background-color:#1a472a;border-radius:10px;padding:20px;text-align:center;margin-bottom:12px">
            <div style="font-size:2rem">🏆</div>
            <div style="font-size:1rem;font-weight:bold;color:#fff;margin-top:8px">Acumule pontos</div>
            <div style="font-size:0.85rem;color:#ccc;margin-top:6px">
                Placar exato vale 5 pontos. Acertar o vencedor ou empate vale 3 pontos.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div style="background-color:#4a1a5c;border-radius:10px;padding:20px;text-align:center;margin-bottom:12px">
            <div style="font-size:2rem">🎁</div>
            <div style="font-size:1rem;font-weight:bold;color:#fff;margin-top:8px">Concorra a prêmios</div>
            <div style="font-size:0.85rem;color:#ccc;margin-top:6px">
                Os três melhores colocados no ranking ganham prêmios.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown("### Como participar?")
st.markdown(
    """
    1. **Crie sua conta** na aba *Login / Cadastro* usando seu email e escolhendo um apelido.
    2. **Registre seus palpites** antes de cada jogo começar — após o apito inicial o prazo encerra.
    3. **Acompanhe o ranking** e veja como você se sai em relação aos outros participantes.
    4. **Torça muito** e boa sorte! 🎉
    """
)

if not st.session_state.get("user_id"):
    st.info("Ainda não tem conta? Clique no link abaixo para se cadastrar.", icon="👤")
    st.page_link("pages/login.py", label="Criar conta / Fazer login", icon="🔐")
