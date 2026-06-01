import streamlit as st

st.set_page_config(
    page_title="Bolão da Copa 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ensure session keys exist
for key in ("user_id", "email", "nickname", "access_token", "refresh_token"):
    if key not in st.session_state:
        st.session_state[key] = None

logged_in = bool(st.session_state["user_id"])

st.logo("assets/logo_sidebar.png", size="large")

st.markdown(
    """
    <style>
    [data-testid="stLogo"] { height: 80px; max-width: 100%; }
    </style>
    """,
    unsafe_allow_html=True,
)

login_page = st.Page("pages/login.py", title="Login / Cadastro", icon="🔐")
palpites_page = st.Page("pages/palpites.py", title="Palpites", icon="⚽")
ranking_page = st.Page("pages/ranking.py", title="Ranking", icon="🏆")
todos_page = st.Page("pages/palpites_todos.py", title="Palpites de Todos", icon="🔍")
admin_page = st.Page("pages/admin.py", title="Painel Admin", icon="🔧")

if logged_in:
    pages = [palpites_page, ranking_page, todos_page, admin_page, login_page]
else:
    pages = [login_page, ranking_page, todos_page]

pg = st.navigation(pages)

# Redirect to palpites after login/register (flag set by login.py)
if logged_in and st.session_state.pop("redirect_to_palpites", False):
    st.switch_page(palpites_page)

pg.run()
