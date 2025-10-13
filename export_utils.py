import io
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

# ---------------------------------------------------
# PERGUNTAS PADRÃO
# ---------------------------------------------------
PERGUNTAS = {
    "p1": "1) Pontos fortes e valores do colega",
    "p2": "2) Palavra-chave que define o colega",
    "p3": "3) Relação com a equipe",
    "j3": "Justificativa Q3",
    "p4": "4) Sua relação com o colega",
    "j4": "Justificativa Q4",
    "p5": "5) Colabora com a equipe?",
    "j5": "Justificativa Q5",
    "p6": "6) Interage com a equipe?",
    "j6": "Justificativa Q6",
    "p7": "7) É proativo?",
    "j7": "Justificativa Q7",
    "p8": "8) Gerencia bem o tempo/tarefas?",
    "j8": "Justificativa Q8",
    "p9": "9) Comunicação com equipe/áreas",
    "j9": "Justificativa Q9",
    "p10": "10) Contribui para resolução de conflitos?",
    "j10": "Justificativa Q10",
    "p11": "11) Contribuição para sucesso da empresa",
    "j11": "Justificativa Q11",
    "p12": "12) Sugestões para desenvolvimento",
    "score": "Pontuação (%)"
}

# ===========================================================
# ============= RELATÓRIOS EXISTENTES (COMPLETOS) ===========
# ===========================================================

def exportar_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        workbook = writer.book
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
        nota_azul = workbook.add_format({
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
        for _, row in df.iterrows():
            worksheet.merge_range(linha, 0, linha, 3, "Relatório de Avaliação Organizacional", titulo_fmt)
            worksheet.set_row(linha, 40)
            linha += 2

            worksheet.write(linha, 0, "Setor", header_fmt)
            worksheet.write(linha, 1, row["setor"], resposta_header_fmt)
            worksheet.write(linha, 2, "Colaborador", header_fmt)
            worksheet.write(linha, 3, row["colaborador"], resposta_header_fmt)
            worksheet.set_row(linha, 30)
            linha += 1

            worksheet.write(linha, 0, "Data", header_fmt)
            worksheet.write(linha, 1, row["data"], resposta_header_fmt)
            worksheet.write(linha, 2, "Pontuação", header_fmt)

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


def exportar_pdf(df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        "titulo",
        parent=styles["Heading1"],
        fontSize=18,
        alignment=1,
        textColor=colors.HexColor("#305496"),
        spaceAfter=20
    )

    def estilo_resposta(valor: str):
        if valor in ["Excelente", "Sim", "Boa"]:
            bg = colors.HexColor("#C6EFCE"); fg = colors.HexColor("#006100")
        elif valor in ["Bom", "Às vezes", "Mais ou menos"]:
            bg = colors.HexColor("#BDD7EE"); fg = colors.HexColor("#1F4E78")
        elif valor in ["Regular"]:
            bg = colors.HexColor("#FFE699"); fg = colors.HexColor("#9C6500")
        elif valor in ["Ruim", "Não", "Nunca"]:
            bg = colors.HexColor("#F8CBAD"); fg = colors.HexColor("#9C0006")
        else:
            bg = colors.white; fg = colors.black
        return bg, fg

    for _, row in df.iterrows():
        elements.append(Paragraph("Relatório de Avaliação Organizacional", titulo_style))
        elements.append(Spacer(1, 12))

        cabecalho = [
            ["Setor", row["setor"], "Colaborador", row["colaborador"]],
            ["Data", row["data"], "Pontuação", f"{row['score']} / 100"]
        ]
        tabela_cabecalho = Table(cabecalho, colWidths=[80, 150, 100, 150])
        tabela_cabecalho.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9E1F2")),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(tabela_cabecalho)
        elements.append(Spacer(1, 14))

        for col, pergunta in PERGUNTAS.items():
            if col in row and col != "score":
                valor = str(row[col])
                bg, fg = estilo_resposta(valor)
                tabela = Table(
                    [[Paragraph(f"<b>{pergunta}</b>", styles["Normal"]),
                      Paragraph(valor, styles["Normal"])]],
                    colWidths=[200, 300]
                )
                tabela.setStyle(TableStyle([
                    ("BACKGROUND", (1, 0), (1, 0), bg),
                    ("TEXTCOLOR", (1, 0), (1, 0), fg),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]))
                elements.append(tabela)
                elements.append(Spacer(1, 6))

        elements.append(Spacer(1, 20))

    doc.build(elements)
    return buffer.getvalue()

# ===========================================================
# ============= RELATÓRIO SIMPLIFICADO (NOVO) ===============
# ===========================================================

def exportar_excel_simplificado(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet("Simplificado")

        titulo_fmt = workbook.add_format({
            "bold": True, "font_size": 22, "align": "center",
            "valign": "vcenter", "fg_color": "#305496",
            "font_color": "white"
        })
        pergunta_fmt = workbook.add_format({
            "bold": True, "font_color": "#1F4E78",
            "align": "left", "valign": "vcenter",
            "font_size": 15, "bg_color": "#D9E1F2", "border": 1
        })
        resposta_fmt = workbook.add_format({
            "text_wrap": True, "valign": "top", "border": 1, "font_size": 13
        })

        linha = 0
        worksheet.merge_range(linha, 0, linha, 3, "Relatório Simplificado de Avaliações", titulo_fmt)
        linha += 2

        for col, pergunta in PERGUNTAS.items():
            if col.startswith("p") and col in df.columns:
                respostas = df[col].dropna().astype(str).tolist()
                if not respostas:
                    continue
                worksheet.write(linha, 0, pergunta, pergunta_fmt)
                linha += 1
                for r in respostas:
                    worksheet.write(linha, 0, f"- {r}", resposta_fmt)
                    linha += 1
                linha += 1

        worksheet.set_column(0, 0, 100)

    return output.getvalue()


def exportar_pdf_simplificado(df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        "titulo",
        parent=styles["Heading1"],
        fontSize=18,
        alignment=1,
        textColor=colors.HexColor("#305496"),
        spaceAfter=20
    )
    pergunta_style = ParagraphStyle(
        "pergunta",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#1F4E78"),
        spaceAfter=6
    )

    elements.append(Paragraph("Relatório Simplificado de Avaliações", titulo_style))
    elements.append(Spacer(1, 12))

    for col, pergunta in PERGUNTAS.items():
        if col.startswith("p") and col in df.columns:
            respostas = df[col].dropna().astype(str).tolist()
            if not respostas:
                continue
            elements.append(Paragraph(pergunta, pergunta_style))
            for r in respostas:
                elements.append(Paragraph(f"• {r}", styles["Normal"]))
            elements.append(Spacer(1, 10))

    doc.build(elements)
    return buffer.getvalue()
