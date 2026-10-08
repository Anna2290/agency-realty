"""Переиспользуемые виджеты UI (DRY-принцип)."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Tuple


def create_labeled_entry(
    parent: tk.Widget,
    label: str,
    row: int,
    column: int = 0,
    width: int = 25,
) -> tk.Entry:
    """Создаёт подпись + поле ввода в grid-сетке.

    Returns:
        Созданный Entry.
    """
    ttk.Label(parent, text=label).grid(row=row, column=column, sticky="w", padx=5, pady=3)
    entry = ttk.Entry(parent, width=width)
    entry.grid(row=row, column=column + 1, sticky="ew", padx=5, pady=3)
    return entry


def create_button(
    parent: tk.Widget,
    text: str,
    command: Callable,
    row: int,
    column: int,
    columnspan: int = 1,
) -> ttk.Button:
    """Создаёт кнопку в grid-сетке."""
    btn = ttk.Button(parent, text=text, command=command)
    btn.grid(row=row, column=column, columnspan=columnspan, padx=5, pady=5, sticky="ew")
    return btn


def create_treeview(
    parent: tk.Widget,
    columns: List[Tuple[str, str, int]],
) -> ttk.Treeview:
    """Создаёт Treeview с колонками.

    Args:
        columns: список (id, заголовок, ширина).
    """
    tree = ttk.Treeview(parent, columns=[c[0] for c in columns], show="headings")
    for col_id, title, width in columns:
        tree.heading(col_id, text=title)
        tree.column(col_id, width=width, anchor="center")
    return tree
