import streamlit as st
import pandas as pd
import datetime
import altair as alt
from db import conectar
from export_utils import exportar_excel, exportar_pdf


def admin_view():

    if "admin_ok" not in st.session_state:
        st.session_state["admin_ok"] = False
    if "perfil" not in st.session_state:
        st.session_state["perfil"] = None

    if not st.session_state["admin_ok"]:
        st.error("⚠️ Acesso negado. Faça login como administrador na tela inicial.")
        return

    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM respostas", conn)

    if df.empty:
        st.info("Nenhuma resposta registrada ainda.")
        return

    st.subheader("🔎 Filtros")
    col1, col2, col3 = st.columns(3)

    with col1:
        filtro_setor = st.selectbox(
            "📂 Filtrar por setor",
            ["Todos"] + sorted(df["setor"].unique().tolist())
        )

    with col2:
        if filtro_setor != "Todos":
            colaboradores_opcoes = df[df["setor"] == filtro_setor]["colaborador"].unique().tolist()
        else:
            colaboradores_opcoes = df["colaborador"].unique().tolist()

        filtro_colaborador = st.selectbox(
            "👥 Filtrar por colaborador",
            ["Todos"] + sorted(colaboradores_opcoes)
        )

    with col3:
        filtro_data = st.selectbox(
            "📅 Filtrar por data",
            ["Todos"] + sorted(df["data"].unique().tolist())
        )

    df_filtrado = df.copy()
    if filtro_setor != "Todos":
        df_filtrado = df_filtrado[df_filtrado["setor"] == filtro_setor]
    if filtro_colaborador != "Todos":
        df_filtrado = df_filtrado[df_filtrado["colaborador"] == filtro_colaborador]
    if filtro_data != "Todos":
        df_filtrado = df_filtrado[df_filtrado["data"] == filtro_data]

    st.subheader("📋 Respostas Registradas")

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="⬇️ Exportar para Excel",
            data=exportar_excel(df_filtrado),
            file_name=f"respostas_{datetime.date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col2:
        st.download_button(
            label="⬇️ Exportar para PDF",
            data=exportar_pdf(df_filtrado),
            file_name=f"respostas_{datetime.date.today()}.pdf",
            mime="application/pdf"
        )

    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

    st.subheader("📊 Resumo Executivo")

    total_respostas = len(df_filtrado)
    media = round(df_filtrado["score"].mean(), 1) if total_respostas > 0 else 0
    maior = df_filtrado["score"].max() if total_respostas > 0 else 0
    menor = df_filtrado["score"].min() if total_respostas > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📑 Nº Respostas", total_respostas)
    col2.metric("📈 Média Geral", f"{media} / 100")
    col3.metric("🥇 Melhor Nota", f"{maior} / 100")
    col4.metric("❌ Pior Nota", f"{menor} / 100")

    if media < 50 and total_respostas > 0:
        st.error("⚠️ Atenção: a média geral está abaixo de 50!")

    if "setor" in df_filtrado.columns and not df_filtrado.empty:
        st.subheader("🏢 Média por Setor")
        df_setor = df_filtrado.groupby("setor")["score"].mean().reset_index()

        chart = alt.Chart(df_setor).mark_bar(color="#4F81BD").encode(
            x=alt.X("setor", sort="-y", title="Setor"),
            y=alt.Y("score", title="Média (%)"),
            tooltip=["setor", "score"]
        )
        st.altair_chart(chart, use_container_width=True)

    st.subheader("🏆 Ranking de Colaboradores")

    if not df_filtrado.empty:
        df_ranking = (
            df_filtrado.groupby("colaborador")["score"]
            .mean()
            .reset_index()
            .sort_values("score", ascending=False)
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔝 Top 5")
            st.table(df_ranking.head(5).reset_index(drop=True))
        with col2:
            st.markdown("### ❌ Bottom 5")
            st.table(df_ranking.tail(5).reset_index(drop=True))
