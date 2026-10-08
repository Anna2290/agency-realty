"""Экспорт коммерческого предложения в PDF (п.4.1.14 ТЗ)."""

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors

from app.config import EXPORT_DIR


def export_offer_to_pdf(client, properties: list, filename: str) -> Path:
    """Формирует PDF-файл коммерческого предложения.

    Args:
        client: объект Client.
        properties: список объектов Property.
        filename: имя выходного файла.

    Returns:
        Path к сохранённому PDF.
    """
    path = EXPORT_DIR / filename
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=16,
        alignment=1,
        spaceAfter=12,
    )

    story = []
    story.append(Paragraph("Коммерческое предложение", title_style))
    story.append(Spacer(1, 0.5 * cm))
    story.append(
        Paragraph(
            f"<b>Клиент:</b> {client.full_name}<br/>"
            f"<b>Телефон:</b> {client.phone}<br/>"
            f"<b>Email:</b> {client.email or '—'}",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 0.5 * cm))

    if not properties:
        story.append(Paragraph("Подходящие объекты не найдены.", styles["Normal"]))
    else:
        data = [["№", "Объект", "Тип", "Площадь, м²", "Этажей", "Цена, ₽"]]
        for i, p in enumerate(properties, start=1):
            data.append(
                [
                    str(i),
                    p.title,
                    p.property_type,
                    f"{p.area:.1f}",
                    str(p.floors),
                    f"{p.price:,.0f}".replace(",", " "),
                ]
            )
        table = Table(data, colWidths=[1 * cm, 6 * cm, 2.5 * cm, 2.5 * cm, 2 * cm, 3 * cm])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                ]
            )
        )
        story.append(table)

    story.append(Spacer(1, 1 * cm))
    story.append(
        Paragraph(
            "С уважением,<br/>Агентство недвижимости «Museum Realty»",
            styles["Normal"],
        )
    )

    doc.build(story)
    return path
