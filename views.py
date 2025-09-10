import streamlit as st
import pandas as pd
from config import ADMIN_PASSWORD
from db import conectar

def admin_view():
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM respostas", conn)

    senha = st.text_input("🔑 Digite a senha de administrador", type="password")

    if senha == ADMIN_PASSWORD:
        st.success("Acesso permitido ✅")

        if not df.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                filtro_setor = st.selectbox("📂 Filtrar por setor", ["Todos"] + sorted(df["setor"].unique().tolist()))
            with col2:
                filtro_colaborador = st.selectbox("👥 Filtrar por colaborador", ["Todos"] + sorted(df["colaborador"].unique().tolist()))
            with col3:
                filtro_data = st.selectbox("📅 Filtrar por data", ["Todos"] + sorted(df["data"].unique().tolist()))

            if filtro_setor != "Todos":
                df = df[df["setor"] == filtro_setor]
            if filtro_colaborador != "Todos":
                df = df[df["colaborador"] == filtro_colaborador]
            if filtro_data != "Todos":
                df = df[df["data"] == filtro_data]

            st.dataframe(df, use_container_width=True)

            st.subheader("📊 Estatísticas")
            st.metric("Média de Pontuação", round(df["score"].mean(), 2))
            st.metric("Maior Pontuação", df["score"].max())
            st.metric("Menor Pontuação", df["score"].min())
        else:
            st.info("Nenhuma resposta registrada ainda.")
    elif senha != "":
        st.error("Senha incorreta ❌")
