import streamlit as st
from .supabase_client import get_supabase, get_admin_supabase


def is_logged_in() -> bool:
    return bool(st.session_state.get("user_id"))


def _load_profile(user_id: str) -> None:
    client = get_admin_supabase()
    try:
        result = (
            client.table("profiles")
            .select("nickname")
            .eq("id", user_id)
            .limit(1)
            .execute()
        )
        if result.data:
            st.session_state["nickname"] = result.data[0]["nickname"]
    except Exception:
        pass


def login(email: str, password: str) -> tuple[bool, str | None]:
    client = get_supabase()
    try:
        resp = client.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state["user_id"] = resp.user.id
        st.session_state["email"] = resp.user.email
        st.session_state["access_token"] = resp.session.access_token
        st.session_state["refresh_token"] = resp.session.refresh_token
        _load_profile(resp.user.id)
        return True, None
    except Exception as exc:
        msg = str(exc)
        if "Invalid login" in msg or "invalid_credentials" in msg:
            return False, "Email ou senha incorretos."
        return False, msg


def register(email: str, password: str, nickname: str) -> tuple[bool, str | None]:
    if not nickname.strip():
        return False, "O apelido não pode estar vazio."
    admin = get_admin_supabase()
    try:
        existing = (
            admin.table("profiles")
            .select("id")
            .eq("nickname", nickname.strip())
            .limit(1)
            .execute()
        )
        if existing.data:
            return False, "Esse apelido já está em uso. Escolha outro."
    except Exception:
        pass
    client = get_supabase()
    try:
        resp = client.auth.sign_up({"email": email, "password": password})
        user = resp.user
        if user is None:
            return False, "Cadastro falhou. Tente novamente."
        admin.table("profiles").insert({"id": user.id, "nickname": nickname.strip()}).execute()
        if resp.session:
            st.session_state["user_id"] = user.id
            st.session_state["email"] = email
            st.session_state["nickname"] = nickname.strip()
            st.session_state["access_token"] = resp.session.access_token
            st.session_state["refresh_token"] = resp.session.refresh_token
        return True, None
    except Exception as exc:
        msg = str(exc)
        if "already registered" in msg or "User already registered" in msg:
            return False, "Este email já está cadastrado."
        return False, msg


def reset_password(email: str) -> tuple[bool, str | None]:
    client = get_supabase()
    try:
        client.auth.reset_password_email(email)
        return True, None
    except Exception as exc:
        return False, str(exc)


def logout() -> None:
    for key in ("user_id", "email", "nickname", "access_token", "refresh_token"):
        st.session_state.pop(key, None)
