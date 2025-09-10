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

            st.subheader("📋 Respostas Registradas")
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.subheader("📊 Estatísticas")

            media = round(df["score"].mean(), 1)
            maior = df["score"].max()
            menor = df["score"].min()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    f"""
                    <div style="background-color:#1f77b4; padding:20px; border-radius:12px; text-align:center; color:white;">
                        <h3>📌 Média</h3>
                        <h2>{media} / 100</h2>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                    <div style="background-color:#2ca02c; padding:20px; border-radius:12px; text-align:center; color:white;">
                        <h3>🏆 Maior Pontuação</h3>
                        <h2>{maior} / 100</h2>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    f"""
                    <div style="background-color:#d62728; padding:20px; border-radius:12px; text-align:center; color:white;">
                        <h3>⬇️ Menor Pontuação</h3>
                        <h2>{menor} / 100</h2>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        else:
            st.info("Nenhuma resposta registrada ainda.")
    elif senha != "":
        st.error("Senha incorreta ❌")
