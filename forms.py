import streamlit as st
from datetime import datetime
from config import SETORES, PESOS
from db import conectar

def formulario():
    conn = conectar()
    cursor = conn.cursor()

    st.title("📋 Pesquisa de Avaliação de Colaboradores")

    setor = st.selectbox("📂 Selecione o setor", list(SETORES.keys()))
    colaborador = st.selectbox("👥 Selecione o funcionário avaliado", SETORES[setor])
    data = datetime.today().strftime("%d/%m/%Y")

    with st.form("pesquisa", clear_on_submit=True):

        st.subheader("✨ Informações iniciais")
        p1 = st.text_area("1️⃣ Pontos fortes e valores do colega", key="p1")
        p2 = st.text_input("2️⃣ Palavra-chave que define o colega", key="p2")

        st.subheader("🤝 Colaboração e Relações")
        p3 = st.radio("3️⃣ Relação com a equipe", list(PESOS["p3"].keys()), horizontal=True, key="p3")
        j3 = st.text_area("Justifique", key="j3")

        p4 = st.radio("4️⃣ Sua relação com o colega", list(PESOS["p4"].keys()), horizontal=True, key="p4")
        j4 = st.text_area("Justifique", key="j4")

        p5 = st.radio("5️⃣ Colabora com a equipe?", list(PESOS["p5"].keys()), horizontal=True, key="p5")
        j5 = st.text_area("Justifique", key="j5")

        st.subheader("🚀 Atitudes e Desempenho")
        p6 = st.radio("6️⃣ Interage com a equipe?", list(PESOS["p6"].keys()), horizontal=True, key="p6")
        j6 = st.text_area("Justifique", key="j6")

        p7 = st.radio("7️⃣ É proativo?", list(PESOS["p7"].keys()), horizontal=True, key="p7")
        j7 = st.text_area("Justifique", key="j7")

        p8 = st.radio("8️⃣ Gerencia bem o tempo/tarefas?", list(PESOS["p8"].keys()), horizontal=True, key="p8")
        j8 = st.text_area("Justifique", key="j8")

        st.subheader("🗣️ Comunicação e Conflitos")
        p9 = st.radio("9️⃣ Comunicação com equipe/áreas", list(PESOS["p9"].keys()), horizontal=True, key="p9")
        j9 = st.text_area("Justifique", key="j9")

        p10 = st.radio("🔟 Contribui para resolução de conflitos?", list(PESOS["p10"].keys()), horizontal=True, key="p10")
        j10 = st.text_area("Justifique", key="j10")

        st.subheader("🏆 Resultados e Sugestões")
        p11 = st.radio("1️⃣1️⃣ Contribuição para sucesso da empresa", list(PESOS["p11"].keys()), horizontal=True, key="p11")
        j11 = st.text_area("Justifique", key="j11")

        p12 = st.text_area("1️⃣2️⃣ Sugestões para desenvolvimento", key="p12")

        mostrar_resumo = st.checkbox("🔎 Visualizar resumo das respostas antes de enviar")

        submitted = st.form_submit_button("✅ Enviar Resposta")

        if submitted:
            obrigatorios = {
                "Pontos fortes": p1,
                "Palavra-chave": p2,
                "Justificativa Q3": j3,
                "Justificativa Q4": j4,
                "Justificativa Q5": j5,
                "Justificativa Q6": j6,
                "Justificativa Q7": j7,
                "Justificativa Q8": j8,
                "Justificativa Q9": j9,
                "Justificativa Q10": j10,
                "Justificativa Q11": j11,
                "Sugestões": p12
            }

            faltando = [campo for campo, valor in obrigatorios.items() if not valor.strip()]

            if faltando:
                st.error(f"⚠️ Os seguintes campos são obrigatórios e precisam ser preenchidos: {', '.join(faltando)}")
            else:
                score_bruto = sum([
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
                score_max = 9 * 4
                score = round((score_bruto / score_max) * 100, 2)

                cursor.execute("""
                INSERT INTO respostas (
                    setor, colaborador, data,
                    p1, p2, p3, j3, p4, j4, p5, j5, p6, j6,
                    p7, j7, p8, j8, p9, j9, p10, j10, p11, j11, p12, score
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (setor, colaborador, data, p1, p2, p3, j3, p4, j4, p5, j5,
                      p6, j6, p7, j7, p8, j8, p9, j9, p10, j10, p11, j11, p12, score))
                conn.commit()

                if mostrar_resumo:
                    st.success("✅ Resposta registrada! Veja abaixo o resumo:")
                    st.write(f"**Setor:** {setor}")
                    st.write(f"**Colaborador avaliado:** {colaborador}")
                    st.write(f"**Data:** {data}")
                    st.write(f"**Pontuação:** {score} / 100")
                    st.write("---")
                    st.write(f"**P1:** {p1}")
                    st.write(f"**P2:** {p2}")
                    st.write(f"**P3:** {p3} | Justificativa: {j3}")
                    st.write(f"**P4:** {p4} | Justificativa: {j4}")
                    st.write(f"**P5:** {p5} | Justificativa: {j5}")
                    st.write(f"**P6:** {p6} | Justificativa: {j6}")
                    st.write(f"**P7:** {p7} | Justificativa: {j7}")
                    st.write(f"**P8:** {p8} | Justificativa: {j8}")
                    st.write(f"**P9:** {p9} | Justificativa: {j9}")
                    st.write(f"**P10:** {p10} | Justificativa: {j10}")
                    st.write(f"**P11:** {p11} | Justificativa: {j11}")
                    st.write(f"**P12:** {p12}")
                else:
                    st.success(f"✅ Resposta registrada com sucesso! Pontuação normalizada: {score}")
