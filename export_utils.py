import io
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

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

def exportar_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet("Relatório")

        azul_escuro = "#132C4A"
        azul_claro = "#D9E1F2"

        titulo_fmt = workbook.add_format({
            "bold": True, "font_size": 22, "align": "center",
            "valign": "vcenter", "fg_color": azul_escuro,
            "font_color": "white"
        })
        header_fmt = workbook.add_format({
            "bold": True, "bg_color": azul_claro, "border": 1,
            "align": "center", "valign": "vcenter", "font_size": 14
        })
        resposta_fmt = workbook.add_format({
            "text_wrap": True, "valign": "top", "border": 1, "font_size": 13
        })
        pergunta_fmt = workbook.add_format({
            "bold": True, "font_color": azul_escuro,
            "align": "left", "valign": "vcenter",
            "font_size": 15, "bg_color": "#F2F2F2", "border": 1
        })

        linha = 0
        for _, row in df.iterrows():
            worksheet.merge_range(linha, 0, linha, 3, "Ω Omega Distribuidora", titulo_fmt)
            linha += 1
            worksheet.merge_range(linha, 0, linha, 3, "Relatório de Avaliação Organizacional", titulo_fmt)
            linha += 2

            worksheet.write(linha, 0, "Setor", header_fmt)
            worksheet.write(linha, 1, row["setor"], resposta_fmt)
            worksheet.write(linha, 2, "Colaborador", header_fmt)
            worksheet.write(linha, 3, row["colaborador"], resposta_fmt)
            linha += 1

            worksheet.write(linha, 0, "Data", header_fmt)
            worksheet.write(linha, 1, row["data"], resposta_fmt)
            worksheet.write(linha, 2, "Pontuação", header_fmt)
            worksheet.write(linha, 3, f"{row['score']} / 100", resposta_fmt)
            linha += 2

            for col, pergunta in PERGUNTAS.items():
                if col in row and col != "score":
                    worksheet.write(linha, 0, pergunta, pergunta_fmt)
                    worksheet.merge_range(linha, 1, linha, 3, str(row[col]), resposta_fmt)
                    linha += 1

            linha += 2

        worksheet.set_column(0, 3, 50)
    return output.getvalue()


def exportar_pdf(df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    azul_escuro = colors.HexColor("#132C4A")
    azul_claro = colors.HexColor("#D9E1F2")

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        "titulo",
        parent=styles["Heading1"],
        fontSize=20,
        alignment=1,
        textColor=azul_escuro,
        spaceAfter=6
    )
    subtitulo_style = ParagraphStyle(
        "subtitulo",
        parent=styles["Heading2"],
        fontSize=13,
        alignment=1,
        textColor=colors.HexColor("#1F4E78"),
        spaceAfter=16
    )
    pergunta_style = ParagraphStyle(
        "pergunta",
        parent=styles["Normal"],
        fontSize=12,
        textColor=azul_escuro,
        spaceAfter=6
    )

    elements.append(Paragraph("Ω Omega Distribuidora", titulo_style))
    elements.append(Paragraph("Relatório de Avaliação Organizacional", subtitulo_style))
    elements.append(HRFlowable(width="100%", color=azul_escuro, thickness=2))
    elements.append(Spacer(1, 10))

    for _, row in df.iterrows():
        elements.append(Paragraph(f"<b>Setor:</b> {row['setor']} | <b>Colaborador:</b> {row['colaborador']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Data:</b> {row['data']} | <b>Pontuação:</b> {row['score']} / 100", styles["Normal"]))
        elements.append(Spacer(1, 10))
        elements.append(HRFlowable(width="100%", color=azul_claro, thickness=1))
        elements.append(Spacer(1, 12))

        for col, pergunta in PERGUNTAS.items():
            if col in row and col != "score":
                elements.append(Paragraph(f"<b>{pergunta}</b>", pergunta_style))
                elements.append(Paragraph(str(row[col]), styles["Normal"]))
                elements.append(Spacer(1, 6))

        elements.append(Spacer(1, 14))
        elements.append(HRFlowable(width="100%", color=azul_escuro, thickness=1))
        elements.append(Spacer(1, 14))

    doc.build(elements)
    return buffer.getvalue()

def exportar_excel_simplificado(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        workbook  = writer.book
        worksheet = workbook.add_worksheet("Simplificado")

        azul_escuro = "#132C4A"
        azul_claro = "#D9E1F2"

        titulo_fmt = workbook.add_format({
            "bold": True, "font_size": 20, "align": "center",
            "valign": "vcenter", "fg_color": azul_escuro,
            "font_color": "white"
        })
        header_fmt = workbook.add_format({
            "bold": True, "font_size": 13, "font_color": azul_escuro
        })
        pergunta_fmt = workbook.add_format({
            "bold": True, "font_color": azul_escuro,
            "align": "left", "valign": "vcenter",
            "font_size": 14, "bg_color": azul_claro, "border": 1
        })
        resposta_fmt = workbook.add_format({
            "text_wrap": True, "valign": "top", "border": 1,
            "font_size": 12
        })
        justificativa_fmt = workbook.add_format({
            "italic": True, "font_color": "#333333",
            "text_wrap": True, "valign": "top", "border": 1,
            "font_size": 11
        })

        linha = 0
        worksheet.merge_range(linha, 0, linha, 2, "Ω Omega Distribuidora", titulo_fmt)
        linha += 1
        worksheet.merge_range(linha, 0, linha, 2, "Relatório Simplificado de Avaliações", titulo_fmt)
        linha += 2

        colaborador = df["colaborador"].iloc[0] if "colaborador" in df.columns else "Colaborador"
        setor = df["setor"].iloc[0] if "setor" in df.columns else "Setor"
        media = round(df["score"].mean(), 2) if "score" in df.columns else 0

        worksheet.write(linha, 0, f"👤 Colaborador: {colaborador}", header_fmt)
        linha += 1
        worksheet.write(linha, 0, f"🏢 Setor: {setor}", header_fmt)
        linha += 1
        worksheet.write(linha, 0, f"📊 Média das Avaliações: {media} / 100", header_fmt)
        linha += 2

        for num in range(1, 13):
            p_col = f"p{num}"
            j_col = f"j{num}"

            if p_col not in df.columns:
                continue
            if j_col not in df.columns:
                df[j_col] = ""

            respostas = df[[p_col, j_col]].dropna(subset=[p_col], how="all")
            if respostas.empty:
                continue

            worksheet.write(linha, 0, PERGUNTAS.get(p_col, f"Pergunta {num}"), pergunta_fmt)
            linha += 1

            for _, row in respostas.iterrows():
                resposta = str(row[p_col])
                justificativa = str(row[j_col])
                worksheet.write(linha, 0, f"• {resposta}", resposta_fmt)
                linha += 1
                if justificativa.strip() not in ["", "nan", "None"]:
                    worksheet.write(linha, 0, f"🗒️ Justificativa: {justificativa}", justificativa_fmt)
                    linha += 1

            linha += 1

        worksheet.set_column(0, 0, 100)
    return output.getvalue()


def exportar_pdf_simplificado(df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    azul_escuro = colors.HexColor("#132C4A")
    azul_claro = colors.HexColor("#D9E1F2")

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        "titulo",
        parent=styles["Heading1"],
        fontSize=20,
        alignment=1,
        textColor=azul_escuro,
        spaceAfter=6
    )
    subtitulo_style = ParagraphStyle(
        "subtitulo",
        parent=styles["Heading2"],
        fontSize=13,
        alignment=1,
        textColor=colors.HexColor("#1F4E78"),
        spaceAfter=16
    )
    pergunta_style = ParagraphStyle(
        "pergunta",
        parent=styles["Normal"],
        fontSize=12,
        textColor=azul_escuro,
        spaceAfter=6,
        leading=15
    )
    resposta_style = ParagraphStyle(
        "resposta",
        parent=styles["Normal"],
        fontSize=11,
        leftIndent=14,
        spaceAfter=3
    )
    justificativa_style = ParagraphStyle(
        "justificativa",
        parent=styles["Normal"],
        fontSize=10,
        leftIndent=20,
        textColor=colors.HexColor("#333333"),
        spaceAfter=4,
        italic=True
    )

    colaborador = df["colaborador"].iloc[0] if "colaborador" in df.columns else "Colaborador"
    setor = df["setor"].iloc[0] if "setor" in df.columns else "Setor"
    media = round(df["score"].mean(), 2) if "score" in df.columns else 0

    elements.append(Paragraph("Ω Omega Distribuidora", titulo_style))
    elements.append(Paragraph("Relatório Simplificado de Avaliações", subtitulo_style))
    elements.append(HRFlowable(width="100%", color=azul_escuro, thickness=2))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"<b>👤 Colaborador:</b> {colaborador}", styles["Normal"]))
    elements.append(Paragraph(f"<b>🏢 Setor:</b> {setor}", styles["Normal"]))
    elements.append(Paragraph(f"<b>📊 Média das Avaliações:</b> {media} / 100", styles["Normal"]))
    elements.append(Spacer(1, 12))
    elements.append(HRFlowable(width="100%", color=azul_claro, thickness=1))
    elements.append(Spacer(1, 10))

    for num in range(1, 13):
        p_col = f"p{num}"
        j_col = f"j{num}"

        if p_col not in df.columns:
            continue
        if j_col not in df.columns:
            df[j_col] = ""

        respostas = df[[p_col, j_col]].dropna(subset=[p_col], how="all")
        if respostas.empty:
            continue

        elements.append(Paragraph(f"<b>{PERGUNTAS.get(p_col, f'Pergunta {num}')}</b>", pergunta_style))
        elements.append(HRFlowable(width="100%", color=azul_claro, thickness=0.5))
        elements.append(Spacer(1, 4))

        for _, row in respostas.iterrows():
            resposta = str(row[p_col])
            justificativa = str(row[j_col])
            elements.append(Paragraph(f"• {resposta}", resposta_style))
            if justificativa.strip() not in ["", "nan", "None"]:
                elements.append(Paragraph(f"🗒️ Justificativa: {justificativa}", justificativa_style))

        elements.append(Spacer(1, 10))

    doc.build(elements)
    return buffer.getvalue()
