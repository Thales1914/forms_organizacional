import streamlit as st
from datetime import datetime
from config import SETORES, PESOS
from db import conectar

def formulario():
    conn = conectar()
    cursor = conn.cursor()

    st.title("📋 Pesquisa de Clima Organizacional")

    setor = st.selectbox("📂 Selecione o setor", list(SETORES.keys()))
    colaborador = st.selectbox("👥 Selecione o funcionário avaliado", SETORES[setor])
    data = datetime.today().strftime("%d/%m/%Y")

    with st.form("pesquisa", clear_on_submit=True):
        p1 = st.text_area("1️⃣ Pontos fortes e valores do colega")
        p2 = st.text_input("2️⃣ Palavra-chave que define o colega")

        p3 = st.radio("3️⃣ Relação com a equipe", list(PESOS["p3"].keys()), horizontal=True)
        j3 = st.text_area("Justifique", key="j3")

        p4 = st.radio("4️⃣ Sua relação com o colega", list(PESOS["p4"].keys()), horizontal=True)
        j4 = st.text_area("Justifique", key="j4")

        p5 = st.radio("5️⃣ Colabora com a equipe?", list(PESOS["p5"].keys()), horizontal=True)
        j5 = st.text_area("Justifique", key="j5")

        p6 = st.radio("6️⃣ Interage com a equipe?", list(PESOS["p6"].keys()), horizontal=True)
        j6 = st.text_area("Justifique", key="j6")

        p7 = st.radio("7️⃣ É proativo?", list(PESOS["p7"].keys()), horizontal=True)
        j7 = st.text_area("Justifique", key="j7")

        p8 = st.radio("8️⃣ Gerencia bem o tempo/tarefas?", list(PESOS["p8"].keys()), horizontal=True)
        j8 = st.text_area("Justifique", key="j8")

        p9 = st.radio("9️⃣ Comunicação com equipe/áreas", list(PESOS["p9"].keys()), horizontal=True)
        j9 = st.text_area("Justifique", key="j9")

        p10 = st.radio("🔟 Contribui para resolução de conflitos?", list(PESOS["p10"].keys()), horizontal=True)
        j10 = st.text_area("Justifique", key="j10")

        p11 = st.radio("1️⃣1️⃣ Contribuição para sucesso da empresa", list(PESOS["p11"].keys()), horizontal=True)
        j11 = st.text_area("Justifique", key="j11")

        p12 = st.text_area("1️⃣2️⃣ Sugestões para desenvolvimento")

        submitted = st.form_submit_button("✅ Enviar Resposta")

        if submitted:
            score = sum([
                PESOS["p3"].get(p3, 0),
                PESOS["p4"].get(p4, 0),
                PESOS["p5"].get(p5, 0),
                PESOS["p6"].get(p6, 0),
                PESOS["p7"].get(p7, 0),
                PESOS["p8"].get(p8, 0),
                PESOS["p9"].get(p9, 0),
                PESOS["p10"].get(p10, 0),
                PESOS["p11"].get(p11, 0),
            ])

            cursor.execute("""
            INSERT INTO respostas (
                setor, colaborador, data,
                p1, p2, p3, j3, p4, j4, p5, j5, p6, j6,
                p7, j7, p8, j8, p9, j9, p10, j10, p11, j11, p12, score
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (setor, colaborador, data, p1, p2, p3, j3, p4, j4, p5, j5,
                  p6, j6, p7, j7, p8, j8, p9, j9, p10, j10, p11, j11, p12, score))
            conn.commit()
            st.success(f"✅ Resposta registrada com sucesso! Pontuação: {score}")
