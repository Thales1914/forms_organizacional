import streamlit as st
import pandas as pd
import datetime
import altair as alt
from db import conectar
from export_utils import exportar_excel

def admin_view():

    if not st.session_state.get("admin_ok", False):
        st.error("⚠️ Acesso negado. Faça login como administrador na tela inicial.")
        return

    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM respostas", conn)

    if not df.empty:

        st.subheader("🔎 Filtros")
        col1, col2, col3 = st.columns(3)
        with col1:
            filtro_setor = st.selectbox(
                "📂 Filtrar por setor",
                ["Todos"] + sorted(df["setor"].unique().tolist())
            )
        with col2:
            filtro_colaborador = st.selectbox(
                "👥 Filtrar por colaborador",
                ["Todos"] + sorted(df["colaborador"].unique().tolist())
            )
        with col3:
            filtro_data = st.selectbox(
                "📅 Filtrar por data",
                ["Todos"] + sorted(df["data"].unique().tolist())
            )

        if filtro_setor != "Todos":
            df = df[df["setor"] == filtro_setor]
        if filtro_colaborador != "Todos":
            df = df[df["colaborador"] == filtro_colaborador]
        if filtro_data != "Todos":
            df = df[df["data"] == filtro_data]

        st.subheader("📋 Respostas Registradas")

        st.download_button(
            label="⬇️ Exportar para Excel",
            data=exportar_excel(df),
            file_name=f"respostas_{datetime.date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("📊 Estatísticas Gerais")

        media = round(df["score"].mean(), 1)
        maior = df["score"].max()
        menor = df["score"].min()

        col1, col2, col3 = st.columns(3)
        col1.metric("Média", f"{media} / 100")
        col2.metric("Maior", f"{maior} / 100")
        col3.metric("Menor", f"{menor} / 100")

        if media < 50:
            st.error("⚠️ Atenção: a média geral está abaixo de 50!")

        st.subheader("📈 Distribuição das Notas")
        chart = alt.Chart(df).mark_bar(color="#4F81BD").encode(
            x=alt.X("score", bin=alt.Bin(maxbins=20), title="Pontuação (%)"),
            y=alt.Y("count()", title="Quantidade"),
            tooltip=["count()", "score"]
        )
        st.altair_chart(chart, use_container_width=True)

        st.subheader("🏆 Destaques")

        try:
            top_col = df.loc[df["score"].idxmax()]
            low_col = df.loc[df["score"].idxmin()]

            col1, col2 = st.columns(2)
            with col1:
                st.success(f"🥇 Melhor avaliação: {top_col['colaborador']} ({top_col['score']} / 100)")
            with col2:
                st.error(f"❌ Pior avaliação: {low_col['colaborador']} ({low_col['score']} / 100)")
        except Exception:
            st.info("Não há dados suficientes para destacar.")

    else:
        st.info("Nenhuma resposta registrada ainda.")
