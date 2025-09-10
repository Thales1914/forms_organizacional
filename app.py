import streamlit as st
from db import inicializar_db
from forms import formulario
from views import admin_view

inicializar_db()

st.sidebar.title("Menu")
modo = st.sidebar.radio("Escolha o modo", ["Responder (Colaborador)", "Ver respostas (Admin)"])

if modo == "Responder (Colaborador)":
    formulario()
else:
    admin_view()
