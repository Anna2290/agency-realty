"""Вкладка «Главная страница» — панель со статистикой и последними объектами."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional

from sqlalchemy.orm import joinedload

from app.database.connection import get_session
from app.database.models import Client, Offer, Property


COLOR_BG_DARK = "#2C3E50"
COLOR_BG_CARD = "#FFFFFF"
COLOR_CARD_STAT = "#B0B0B0"
COLOR_TEXT = "#000000"
COLOR_TEXT_HEADER = "#333333"
COLOR_BORDER = "#E0E0E0"


class DashboardView:
    """Главная страница приложения с обзором (Frame 5)."""

    def __init__(
        self,
        parent: ttk.Notebook,
        username: str = "Менеджер",
        on_add_property: Optional[Callable] = None,
        on_open_search: Optional[Callable] = None,
    ) -> None:
        self.username = username
        self.on_add_property = on_add_property
        self.on_open_search = on_open_search

        self.frame = tk.Frame(parent, bg=COLOR_BG_DARK)

        self.card = tk.Frame(self.frame, bg=COLOR_BG_CARD)
        self.card.pack(fill="both", expand=True, padx=20, pady=20)

        self._stat_labels: dict = {}

        self._build_header()
        self._build_stats_cards()
        self._build_recent_table()
        self._build_footer()

    # -------- Шапка --------

    def _build_header(self) -> None:
        header = tk.Frame(self.card, bg=COLOR_BG_CARD, height=50)
        header.pack(fill="x", padx=20, pady=(15, 5))
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🏠  Главная страница",
            font=("Arial", 12, "bold"),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(side="left")

        tk.Label(
            header,
            text=f"👤  {self.username}",
            font=("Arial", 12),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(side="right")

        tk.Frame(self.card, bg=COLOR_BORDER, height=1).pack(fill="x", padx=20, pady=(5, 15))

    # -------- Статистика --------

    def _get_stats(self) -> dict:
        session = get_session()
        try:
            return {
                "objects": session.query(Property).count(),
                "requests": session.query(Offer).count(),
                "deals": session.query(Property)
                .filter(Property.status.in_(["продано", "сдано", "сделка"]))
                .count(),
                "clients": session.query(Client).count(),
            }
        finally:
            session.close()

    def _build_stats_cards(self) -> None:
        stats = self._get_stats()
        cards_data = [
            ("objects", "Объект", stats["objects"]),
            ("requests", "Заявки", stats["requests"]),
            ("deals", "Сделки", stats["deals"]),
            ("clients", "Клиенты", stats["clients"]),
        ]

        container = tk.Frame(self.card, bg=COLOR_BG_CARD)
        container.pack(fill="x", padx=30, pady=(0, 25))

        for key, title, value in cards_data:
            card = tk.Frame(container, bg=COLOR_CARD_STAT, width=100, height=80)
            card.pack(side="left", padx=10)
            card.pack_propagate(False)

            value_label = tk.Label(
                card,
                text=str(value),
                font=("Arial", 16, "bold"),
                bg=COLOR_CARD_STAT,
                fg=COLOR_TEXT,
            )
            value_label.pack(pady=(15, 3))
            self._stat_labels[key] = value_label

            tk.Label(
                card,
                text=title,
                font=("Arial", 10),
                bg=COLOR_CARD_STAT,
                fg=COLOR_TEXT,
            ).pack()

    # -------- Таблица --------

    def _get_recent_properties(self, limit: int = 5) -> List[dict]:
        session = get_session()
        try:
            props = (
                session.query(Property)
                .options(joinedload(Property.district))
                .order_by(Property.created_at.desc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "id": p.id,
                    "address": p.address,
                    "district": p.district.name if p.district else "—",
                    "price": p.price,
                }
                for p in props
            ]
        finally:
            session.close()

    def _build_recent_table(self) -> None:
        tk.Label(
            self.card,
            text="Последние добавленные объекты",
            font=("Arial", 11, "bold"),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT_HEADER,
        ).pack(anchor="w", padx=30, pady=(0, 10))

        table_frame = tk.Frame(self.card, bg=COLOR_BG_CARD)
        table_frame.pack(fill="both", expand=True, padx=30)

        columns = [
            ("id", "ID", 70),
            ("address", "Адрес", 240),
            ("district", "Район", 120),
            ("price", "Цена", 100),
        ]

        style = ttk.Style()
        style.configure(
            "Dashboard.Treeview",
            font=("Arial", 11),
            rowheight=30,
            background=COLOR_BG_CARD,
            fieldbackground=COLOR_BG_CARD,
        )
        style.configure(
            "Dashboard.Treeview.Heading",
            font=("Arial", 11, "bold"),
            background=COLOR_BG_CARD,
            foreground=COLOR_TEXT,
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=[c[0] for c in columns],
            show="headings",
            style="Dashboard.Treeview",
            height=5,
        )
        for col_id, col_title, width in columns:
            self.tree.heading(col_id, text=col_title)
            self.tree.column(col_id, width=width, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self._refresh_table()

    def _refresh_table(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        for prop in self._get_recent_properties(limit=5):
            price_text = f"{prop['price']:,.0f}".replace(",", " ")
            self.tree.insert(
                "",
                "end",
                values=(prop["id"], prop["address"], prop["district"], price_text),
            )

    # -------- Футер --------

    def _build_footer(self) -> None:
        tk.Frame(self.card, bg=COLOR_BORDER, height=1).pack(fill="x", padx=30, pady=(15, 0))

        footer = tk.Frame(self.card, bg=COLOR_BG_CARD, height=50)
        footer.pack(fill="x", side="bottom", padx=30, pady=(10, 20))
        footer.pack_propagate(False)

        tk.Button(
            footer,
            text="[ +  Добавить объект ]",
            font=("Arial", 11),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
            bd=0,
            relief="flat",
            cursor="hand2",
            activebackground="#EFEFEF",
            command=self._handle_add,
        ).pack(side="left", pady=10)

        tk.Button(
            footer,
            text="[ 🔍  Подобрать ]",
            font=("Arial", 11),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
            bd=0,
            relief="flat",
            cursor="hand2",
            activebackground="#EFEFEF",
            command=self._handle_search,
        ).pack(side="right", pady=10)

    def _handle_add(self) -> None:
        if self.on_add_property:
            self.on_add_property()

    def _handle_search(self) -> None:
        if self.on_open_search:
            self.on_open_search()

    def refresh(self) -> None:
        stats = self._get_stats()
        for key, label in self._stat_labels.items():
            label.configure(text=str(stats.get(key, 0)))
        self._refresh_table()
