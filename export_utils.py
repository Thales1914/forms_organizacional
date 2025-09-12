import io
import pandas as pd

PERGUNTAS = {
    "p1": "1️⃣ Pontos fortes e valores do colega",
    "p2": "2️⃣ Palavra-chave que define o colega",
    "p3": "3️⃣ Relação com a equipe",
    "j3": "Justificativa Q3",
    "p4": "4️⃣ Sua relação com o colega",
    "j4": "Justificativa Q4",
    "p5": "5️⃣ Colabora com a equipe?",
    "j5": "Justificativa Q5",
    "p6": "6️⃣ Interage com a equipe?",
    "j6": "Justificativa Q6",
    "p7": "7️⃣ É proativo?",
    "j7": "Justificativa Q7",
    "p8": "8️⃣ Gerencia bem o tempo/tarefas?",
    "j8": "Justificativa Q8",
    "p9": "9️⃣ Comunicação com equipe/áreas",
    "j9": "Justificativa Q9",
    "p10": "🔟 Contribui para resolução de conflitos?",
    "j10": "Justificativa Q10",
    "p11": "1️⃣1️⃣ Contribuição para sucesso da empresa",
    "j11": "Justificativa Q11",
    "p12": "1️⃣2️⃣ Sugestões para desenvolvimento",
    "score": "Pontuação (%)"
}

def exportar_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        workbook  = writer.book
        worksheet = workbook.add_worksheet("Relatório")

        titulo_fmt = workbook.add_format({
            "bold": True, "font_size": 22,
            "align": "center", "valign": "vcenter",
            "fg_color": "#305496", "font_color": "white"
        })
        header_fmt = workbook.add_format({
            "bold": True, "bg_color": "#D9E1F2", "border": 1,
            "align": "center", "valign": "vcenter", "font_size": 14
        })
        resposta_header_fmt = workbook.add_format({
            "bold": True, "border": 1, "align": "center",
            "valign": "vcenter", "font_size": 14
        })
        pergunta_fmt = workbook.add_format({
            "bold": True, "font_color": "#1F4E78",
            "align": "left", "valign": "vcenter",
            "font_size": 15, "bg_color": "#F2F2F2", "border": 1
        })
        resposta_fmt = workbook.add_format({
            "text_wrap": True, "valign": "top",
            "border": 1, "font_size": 13
        })

        nota_verde = workbook.add_format({
            "bg_color": "#C6EFCE", "font_color": "#006100",
            "border": 1, "bold": True, "align": "center",
            "valign": "vcenter", "font_size": 16
        })
        nota_azul  = workbook.add_format({
            "bg_color": "#BDD7EE", "font_color": "#1F4E78",
            "border": 1, "bold": True, "align": "center",
            "valign": "vcenter", "font_size": 16
        })
        nota_laranja = workbook.add_format({
            "bg_color": "#FFE699", "font_color": "#9C6500",
            "border": 1, "bold": True, "align": "center",
            "valign": "vcenter", "font_size": 16
        })
        nota_vermelha = workbook.add_format({
            "bg_color": "#F8CBAD", "font_color": "#9C0006",
            "border": 1, "bold": True, "align": "center",
            "valign": "vcenter", "font_size": 16
        })

        score_fmt_verde = workbook.add_format({
            "bg_color": "#C6EFCE", "font_color": "#006100",
            "border": 1, "bold": True, "align": "center",
            "valign": "vcenter", "font_size": 20
        })
        score_fmt_laranja = workbook.add_format({
            "bg_color": "#FFE699", "font_color": "#9C6500",
            "border": 1, "bold": True, "align": "center",
            "valign": "vcenter", "font_size": 20
        })
        score_fmt_vermelho = workbook.add_format({
            "bg_color": "#F8CBAD", "font_color": "#9C0006",
            "border": 1, "bold": True, "align": "center",
            "valign": "vcenter", "font_size": 20
        })

        def estilo_nota(valor: str):
            if valor in ["Excelente", "Sim", "Boa"]:
                return nota_verde
            elif valor in ["Bom", "Às vezes", "Mais ou menos"]:
                return nota_azul
            elif valor in ["Regular"]:
                return nota_laranja
            elif valor in ["Ruim", "Não", "Nunca"]:
                return nota_vermelha
            return resposta_fmt

        linha = 0
        for idx, row in df.iterrows():

            worksheet.merge_range(linha, 0, linha, 3,
                                  "Relatório de Avaliação Organizacional",
                                  titulo_fmt)
            worksheet.set_row(linha, 40)  
            linha += 2

            worksheet.write(linha, 0, "📂 Setor", header_fmt)
            worksheet.write(linha, 1, row["setor"], resposta_header_fmt)
            worksheet.write(linha, 2, "👥 Colaborador", header_fmt)
            worksheet.write(linha, 3, row["colaborador"], resposta_header_fmt)
            worksheet.set_row(linha, 30)
            linha += 1

            worksheet.write(linha, 0, "📅 Data", header_fmt)
            worksheet.write(linha, 1, row["data"], resposta_header_fmt)
            worksheet.write(linha, 2, "⭐ Pontuação", header_fmt)

            score_val = row["score"]
            if score_val >= 75:
                score_fmt = score_fmt_verde
            elif score_val >= 50:
                score_fmt = score_fmt_laranja
            else:
                score_fmt = score_fmt_vermelho
            worksheet.write(linha, 3, f"{score_val} / 100", score_fmt)
            worksheet.set_row(linha, 35)
            linha += 2

            # === Perguntas e respostas ===
            for col, pergunta in PERGUNTAS.items():
                if col in row and col != "score":
                    worksheet.write(linha, 0, pergunta, pergunta_fmt)
                    valor = str(row[col])
                    fmt = estilo_nota(valor)
                    worksheet.merge_range(linha, 1, linha, 3, valor, fmt)
                    worksheet.set_row(linha, 30)
                    linha += 1

            linha += 1

        worksheet.set_column(0, 0, 65)
        worksheet.set_column(1, 3, 55)
        worksheet.set_paper(9)
        worksheet.fit_to_pages(1, 1)

    return output.getvalue()
