"""Утилита для рисования прямоугольников со скруглёнными углами на Canvas.

Tkinter не поддерживает закругления «из коробки» — используем
create_polygon(smooth=True) для имитации скругления.
"""

from tkinter import Canvas


def draw_round_rect(
    canvas: Canvas,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    radius: float = 20,
    **kwargs,
):
    """Рисует прямоугольник со скруглёнными углами.

    Args:
        canvas: объект Canvas, на котором рисуем.
        x1, y1: верхний левый угол.
        x2, y2: нижний правый угол.
        radius: радиус скругления.
        **kwargs: передаются в create_polygon (fill, outline, width и т.д.).

    Returns:
        id созданной фигуры на Canvas.
    """
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)
