import os
import streamlit as st
from db import inicializar_db
from forms import formulario
from views import admin_view
from config import get_admin_password

inicializar_db()

st.set_page_config(
    page_title="Pesquisa de Avaliação de Colaboradores",
    layout="centered",
    page_icon="📋"
)

if "perfil" not in st.session_state:
    st.session_state["perfil"] = None
if "admin_ok" not in st.session_state:
    st.session_state["admin_ok"] = False

if st.session_state["perfil"] is None:
    caminho_logo = os.path.join(os.path.dirname(__file__), "assets", "logo.jpeg")

    st.image(caminho_logo, use_container_width=True)

    st.markdown("<h1 style='text-align: center;'>📋 Pesquisa de Avaliação de Colaboradores</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Menu Principal</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🙋‍♂️ Colaborador", use_container_width=True, type="primary"):
            st.session_state["perfil"] = "Colaborador"
            st.rerun()

    with col2:
        senha = st.text_input("🔑 Senha de administrador", type="password")
        if st.button("⚙️ Admin", use_container_width=True, type="secondary"):
            if senha == get_admin_password():
                st.session_state["perfil"] = "Admin"
                st.session_state["admin_ok"] = True
                st.success("✅ Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Senha incorreta ❌")

elif st.session_state["perfil"] == "Colaborador":
    st.sidebar.title("Menu")
    st.sidebar.info("👥 Modo Colaborador")
    formulario()

    if st.sidebar.button("⬅️ Sair"):
        st.session_state["perfil"] = None
        st.session_state["admin_ok"] = False
        st.rerun()

elif st.session_state["perfil"] == "Admin":
    st.sidebar.title("Menu")
    st.sidebar.info("⚙️ Modo Administrador")

    if st.session_state["admin_ok"]:
        admin_view()
    else:
        st.error("Acesso negado ❌")

    if st.sidebar.button("⬅️ Sair"):
        st.session_state["perfil"] = None
        st.session_state["admin_ok"] = False
        st.rerun()
