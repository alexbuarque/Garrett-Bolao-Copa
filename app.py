import streamlit as st

st.set_page_config(
    page_title="Ação entre amigos — Copa 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ensure session keys exist
for key in ("user_id", "email", "nickname", "access_token", "refresh_token"):
    if key not in st.session_state:
        st.session_state[key] = None

logged_in = bool(st.session_state["user_id"])

st.logo("assets/logo_sidebar.png")

st.markdown(
    """
    <style>
    [data-testid="stLogo"] { height: 80px; max-width: 100%; }
    </style>
    """,
    unsafe_allow_html=True,
)

home_page = st.Page("pages/home.py", title="Início", icon="🏠")
login_page = st.Page("pages/login.py", title="Login / Cadastro", icon="🔐")
palpites_page = st.Page("pages/palpites.py", title="Palpites", icon="⚽")
ranking_page = st.Page("pages/ranking.py", title="Ranking", icon="🏆")
todos_page = st.Page("pages/palpites_todos.py", title="Palpites de Todos", icon="🔍")
calendario_page = st.Page("pages/calendario.py", title="Calendário", icon="📅")
regras_page = st.Page("pages/regras.py", title="Regras", icon="📋")
admin_page = st.Page("pages/admin.py", title="Painel Admin", icon="🔧")

if logged_in:
    pages = [home_page, palpites_page, ranking_page, todos_page, calendario_page, regras_page, admin_page, login_page]
else:
    # Include palpites_page so an expired session at /palpites doesn't flash "Page not found".
    # palpites.py has its own auth check and shows a login prompt instead.
    pages = [home_page, login_page, palpites_page, ranking_page, todos_page, calendario_page, regras_page]

pg = st.navigation(pages)

# Redirect password reset links to login page where the reset form lives
if st.query_params.get("type") == "recovery":
    st.switch_page(login_page)

# Redirect to palpites after login/register (flag set by login.py)
if logged_in and st.session_state.pop("redirect_to_palpites", False):
    st.switch_page(palpites_page)

pg.run()
