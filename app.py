import streamlit as st
from db import inicializar_db
from forms import formulario
from views import admin_view
from config import ADMIN_PASSWORD

inicializar_db()

st.set_page_config(
    page_title="Pesquisa de Avaliação de Colaboradores",
    layout="centered",
    page_icon="📋"
)

if "perfil" not in st.session_state:
    st.session_state.perfil = None
if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False

if st.session_state.perfil is None:
    st.title("📋Pesquisa de Avaliação de Colaboradores")
    st.subheader("Menu Principal")

    escolha = st.radio("Você é:", ["Colaborador", "Admin"])

    if escolha == "Colaborador":
        if st.button("Entrar como Colaborador"):
            st.session_state.perfil = "Colaborador"
            st.rerun()

    elif escolha == "Admin":
        senha = st.text_input("🔑 Senha de administrador", type="password")
        if st.button("Entrar como Admin"):
            if senha == ADMIN_PASSWORD:
                st.session_state.perfil = "Admin"
                st.session_state.admin_ok = True
                st.rerun()
            else:
                st.error("Senha incorreta ❌")

elif st.session_state.perfil == "Colaborador":
    st.sidebar.title("Menu")
    st.sidebar.info("👥 Modo Colaborador")
    formulario()
    if st.sidebar.button("Sair"):
        st.session_state.perfil = None
        st.session_state.admin_ok = False
        st.rerun()

elif st.session_state.perfil == "Admin":
    st.sidebar.title("Menu")
    st.sidebar.info("⚙️ Modo Administrador")

    if st.session_state.admin_ok:
        admin_view()
    else:
        st.error("Acesso negado ❌")

    if st.sidebar.button("Sair"):
        st.session_state.perfil = None
        st.session_state.admin_ok = False
        st.rerun()
