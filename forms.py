import streamlit as st
from datetime import datetime, date
from config import SETORES, PESOS
from db import conectar


def formulario():
    conn = conectar()
    if conn is None:
        st.error("Não foi possível conectar ao banco de dados.")
        return

    cursor = conn.cursor()

    st.title("📋 Pesquisa de Avaliação de Colaboradores")

    if "setor" not in st.session_state:
        st.session_state["setor"] = list(SETORES.keys())[0]
    if "colaborador" not in st.session_state:
        st.session_state["colaborador"] = SETORES[st.session_state["setor"]][0]
    if "respostas" not in st.session_state:
        st.session_state["respostas"] = {}

    setor = st.selectbox(
        "📂 Selecione o setor",
        list(SETORES.keys()),
        index=list(SETORES.keys()).index(st.session_state["setor"]),
        key="setor"
    )

    colaborador = st.selectbox(
        "👥 Selecione o funcionário avaliado",
        SETORES[setor],
        index=SETORES[setor].index(st.session_state["colaborador"]) if st.session_state["colaborador"] in SETORES[setor] else 0,
        key="colaborador"
    )

    data = date.today()  # grava no formato DATE do Postgres

    with st.form("pesquisa", clear_on_submit=True):
        respostas = {}

        st.subheader("✨ Informações gerais")
        respostas["p1"] = st.text_area("1) Pontos fortes e valores do colega", value=st.session_state["respostas"].get("p1", ""))
        respostas["p2"] = st.text_input("2) Palavra-chave que define o colega", value=st.session_state["respostas"].get("p2", ""))

        total_perguntas = 11
        progresso = 0

        # =======================
        # BLOCO DE PERGUNTAS
        # =======================
        st.subheader("🤝 Colaboração e Relações")
        respostas["p3"] = st.radio("3) Relação com a equipe", list(PESOS["p3"].keys()), horizontal=True,
                                   index=list(PESOS["p3"].keys()).index(st.session_state["respostas"].get("p3", list(PESOS["p3"].keys())[0])))
        respostas["j3"] = st.text_area("Justifique (Q3)", value=st.session_state["respostas"].get("j3", ""))
        progresso += 1
        st.progress(progresso / total_perguntas)

        respostas["p4"] = st.radio("4) Sua relação com o colega", list(PESOS["p4"].keys()), horizontal=True,
                                   index=list(PESOS["p4"].keys()).index(st.session_state["respostas"].get("p4", list(PESOS["p4"].keys())[0])))
        respostas["j4"] = st.text_area("Justifique (Q4)", value=st.session_state["respostas"].get("j4", ""))
        progresso += 1
        st.progress(progresso / total_perguntas)

        respostas["p5"] = st.radio("5) Colabora com a equipe?", list(PESOS["p5"].keys()), horizontal=True,
                                   index=list(PESOS["p5"].keys()).index(st.session_state["respostas"].get("p5", list(PESOS["p5"].keys())[0])))
        respostas["j5"] = st.text_area("Justifique (Q5)", value=st.session_state["respostas"].get("j5", ""))
        progresso += 1
        st.progress(progresso / total_perguntas)

        st.subheader("🚀 Atitudes e Desempenho")
        respostas["p6"] = st.radio("6) Interage com a equipe?", list(PESOS["p6"].keys()), horizontal=True,
                                   index=list(PESOS["p6"].keys()).index(st.session_state["respostas"].get("p6", list(PESOS["p6"].keys())[0])))
        respostas["j6"] = st.text_area("Justifique (Q6)", value=st.session_state["respostas"].get("j6", ""))
        progresso += 1
        st.progress(progresso / total_perguntas)

        respostas["p7"] = st.radio("7) É proativo?", list(PESOS["p7"].keys()), horizontal=True,
                                   index=list(PESOS["p7"].keys()).index(st.session_state["respostas"].get("p7", list(PESOS["p7"].keys())[0])))
        respostas["j7"] = st.text_area("Justifique (Q7)", value=st.session_state["respostas"].get("j7", ""))
        progresso += 1
        st.progress(progresso / total_perguntas)

        respostas["p8"] = st.radio("8) Gerencia bem o tempo/tarefas?", list(PESOS["p8"].keys()), horizontal=True,
                                   index=list(PESOS["p8"].keys()).index(st.session_state["respostas"].get("p8", list(PESOS["p8"].keys())[0])))
        respostas["j8"] = st.text_area("Justifique (Q8)", value=st.session_state["respostas"].get("j8", ""))
        progresso += 1
        st.progress(progresso / total_perguntas)

        st.subheader("🗣️ Comunicação e Conflitos")
        respostas["p9"] = st.radio("9) Comunicação com equipe/áreas", list(PESOS["p9"].keys()), horizontal=True,
                                   index=list(PESOS["p9"].keys()).index(st.session_state["respostas"].get("p9", list(PESOS["p9"].keys())[0])))
        respostas["j9"] = st.text_area("Justifique (Q9)", value=st.session_state["respostas"].get("j9", ""))
        progresso += 1
        st.progress(progresso / total_perguntas)

        respostas["p10"] = st.radio("10) Contribui para resolução de conflitos?", list(PESOS["p10"].keys()), horizontal=True,
                                    index=list(PESOS["p10"].keys()).index(st.session_state["respostas"].get("p10", list(PESOS["p10"].keys())[0])))
        respostas["j10"] = st.text_area("Justifique (Q10)", value=st.session_state["respostas"].get("j10", ""))
        progresso += 1
        st.progress(progresso / total_perguntas)

        st.subheader("🏆 Resultados e Sugestões")
        respostas["p11"] = st.radio("11) Contribuição para sucesso da empresa", list(PESOS["p11"].keys()), horizontal=True,
                                    index=list(PESOS["p11"].keys()).index(st.session_state["respostas"].get("p11", list(PESOS["p11"].keys())[0])))
        respostas["j11"] = st.text_area("Justifique (Q11)", value=st.session_state["respostas"].get("j11", ""))
        progresso += 1
        st.progress(progresso / total_perguntas)

        respostas["p12"] = st.text_area("12) Sugestões para desenvolvimento", value=st.session_state["respostas"].get("p12", ""))

        mostrar_resumo = st.checkbox("🔎 Visualizar resumo das respostas antes de enviar")
        submitted = st.form_submit_button("✅ Enviar Resposta")

        if submitted:
            obrigatorios = {k: v for k, v in respostas.items() if not v.strip() and not k.startswith("j")}
            if obrigatorios:
                st.error("⚠️ Existem campos obrigatórios que precisam ser preenchidos.")
            else:
                score_bruto = sum([
                    PESOS["p3"].get(respostas["p3"], 0),
                    PESOS["p4"].get(respostas["p4"], 0),
                    PESOS["p5"].get(respostas["p5"], 0),
                    PESOS["p6"].get(respostas["p6"], 0),
                    PESOS["p7"].get(respostas["p7"], 0),
                    PESOS["p8"].get(respostas["p8"], 0),
                    PESOS["p9"].get(respostas["p9"], 0),
                    PESOS["p10"].get(respostas["p10"], 0),
                    PESOS["p11"].get(respostas["p11"], 0),
                ])
                score = round((score_bruto / (9 * 4)) * 100, 2)

                cursor.execute("""
                INSERT INTO respostas (
                    setor, colaborador, data,
                    p1, p2, p3, j3, p4, j4, p5, j5, p6, j6,
                    p7, j7, p8, j8, p9, j9, p10, j10, p11, j11, p12, score
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    setor, colaborador, data,
                    respostas["p1"], respostas["p2"], respostas["p3"], respostas["j3"],
                    respostas["p4"], respostas["j4"], respostas["p5"], respostas["j5"],
                    respostas["p6"], respostas["j6"], respostas["p7"], respostas["j7"],
                    respostas["p8"], respostas["j8"], respostas["p9"], respostas["j9"],
                    respostas["p10"], respostas["j10"], respostas["p11"], respostas["j11"],
                    respostas["p12"], score
                ))
                conn.commit()
                cursor.close()
                conn.close()

                st.session_state["respostas"] = {}

                if mostrar_resumo:
                    st.success("✅ Resposta registrada! Veja abaixo o resumo:")
                    for k, v in respostas.items():
                        st.write(f"**{k.upper()}**: {v}")
                    st.write(f"**Pontuação final:** {score} / 100")
                else:
                    st.success(f"✅ Resposta registrada com sucesso! Pontuação final: {score} / 100")
