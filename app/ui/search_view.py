"""Вкладка «Подобрать» — поиск объектов недвижимости (Frame 7).

Кнопка [ ← Назад ] переключает на вкладку «Главная».
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional

from app.logic.search_service import SearchService
from app.logic.property_service import PropertyService
from app.utils.validators import parse_float, parse_int


COLOR_BG_DARK = "#2C3E50"
COLOR_BG_CARD = "#FFFFFF"
COLOR_BG_PANEL = "#B0B0B0"
COLOR_TEXT = "#000000"
COLOR_BORDER = "#DDDDDD"
COLOR_CARD_ITEM = "#F5F5F5"
COLOR_BTN = "#DDDDDD"

PHOTO_COLORS = [
    "#4A90E2",
    "#50E3C2",
    "#F5A623",
    "#B8E986",
    "#9013FE",
    "#F8E71C",
    "#D0021B",
    "#7ED321",
]


class SearchView:
    """Вкладка «Подобрать» — карточки объектов (Frame 7)."""

    def __init__(
        self,
        parent: ttk.Notebook,
        on_back: Optional[Callable] = None,
    ) -> None:
        """Создаёт вкладку.

        Args:
            parent: родительский Notebook.
            on_back: колбэк для кнопки [ ← Назад ]
                     (переключение на «Главную»).
        """
        self.search_service = SearchService()
        self.property_service = PropertyService()
        self.on_back = on_back

        self.frame = tk.Frame(parent, bg=COLOR_BG_DARK)

        self.card = tk.Frame(self.frame, bg=COLOR_BG_CARD)
        self.card.pack(fill="both", expand=True, padx=25, pady=25)

        self._build_header()
        self._build_filters()
        self._build_cards_grid()
        self._on_search()

    # ---------------- Шапка ----------------

    def _build_header(self) -> None:
        header = tk.Frame(self.card, bg=COLOR_BG_CARD, height=40)
        header.pack(fill="x", padx=20, pady=(15, 5))
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🧭   Подобрать",
            font=("Arial", 11),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(side="left")

        # Кнопка «Назад» — теперь рабочая
        back_btn = tk.Label(
            header,
            text="[ ← Назад ]",
            font=("Arial", 10),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
            cursor="hand2",
        )
        back_btn.pack(side="right")
        back_btn.bind("<Button-1>", lambda e: self._on_back_click())

        tk.Frame(self.card, bg=COLOR_BORDER, height=1).pack(fill="x", padx=20, pady=(5, 10))

        self.found_label = tk.Label(
            self.card,
            text="Найдено 0 объектов",
            font=("Arial", 10),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        )
        self.found_label.pack(anchor="w", padx=20, pady=(5, 10))

    def _on_back_click(self) -> None:
        """Обработчик кнопки «Назад» — вернуться на Главную."""
        if self.on_back:
            self.on_back()

    # ---------------- Фильтры ----------------

    def _build_filters(self) -> None:
        tk.Label(
            self.card, text="ФИЛЬТРЫ", font=("Arial", 10, "bold"), bg=COLOR_BG_CARD, fg=COLOR_TEXT
        ).pack(pady=(0, 5))

        panel = tk.Frame(self.card, bg=COLOR_BG_PANEL)
        panel.pack(fill="x", padx=20, pady=(0, 10))

        row1 = tk.Frame(panel, bg=COLOR_BG_PANEL)
        row1.pack(fill="x", padx=10, pady=(8, 4))

        self.deal_combo = self._combo(row1, ["Купить", "Снять", "Продажа", "Аренда"])
        self.type_combo = self._combo(row1, ["Квартира", "Дом", "Помещение"])
        districts = ["Все районы"] + [d.name for d in self.property_service.get_districts()]
        self.district_combo = self._combo(row1, districts)

        row2 = tk.Frame(panel, bg=COLOR_BG_PANEL)
        row2.pack(fill="x", padx=10, pady=3)
        tk.Label(row2, text="Цена:", font=("Arial", 10), bg=COLOR_BG_PANEL, fg=COLOR_TEXT).pack(
            side="left"
        )
        self.price_min = tk.Entry(
            row2, font=("Arial", 10), bd=0, relief="flat", bg="#FFFFFF", fg=COLOR_TEXT, width=14
        )
        self.price_min.insert(0, "0")
        self.price_min.pack(side="left", padx=(5, 5), ipady=4)
        tk.Label(row2, text="—", font=("Arial", 10), bg=COLOR_BG_PANEL, fg=COLOR_TEXT).pack(
            side="left"
        )
        self.price_max = tk.Entry(
            row2, font=("Arial", 10), bd=0, relief="flat", bg="#FFFFFF", fg=COLOR_TEXT, width=16
        )
        self.price_max.insert(0, "50000000")
        self.price_max.pack(side="left", padx=(5, 0), ipady=4)

        row3 = tk.Frame(panel, bg=COLOR_BG_PANEL)
        row3.pack(fill="x", padx=10, pady=3)
        tk.Label(row3, text="Площадь:", font=("Arial", 10), bg=COLOR_BG_PANEL, fg=COLOR_TEXT).pack(
            side="left"
        )
        self.area_min = tk.Entry(
            row3, font=("Arial", 10), bd=0, relief="flat", bg="#FFFFFF", fg=COLOR_TEXT, width=8
        )
        self.area_min.insert(0, "10")
        self.area_min.pack(side="left", padx=(5, 5), ipady=4)
        tk.Label(row3, text="—", font=("Arial", 10), bg=COLOR_BG_PANEL, fg=COLOR_TEXT).pack(
            side="left"
        )
        self.area_max = tk.Entry(
            row3, font=("Arial", 10), bd=0, relief="flat", bg="#FFFFFF", fg=COLOR_TEXT, width=8
        )
        self.area_max.insert(0, "500")
        self.area_max.pack(side="left", padx=(5, 5), ipady=4)
        tk.Label(row3, text="м²", font=("Arial", 10), bg=COLOR_BG_PANEL, fg=COLOR_TEXT).pack(
            side="left"
        )

        row4 = tk.Frame(panel, bg=COLOR_BG_PANEL)
        row4.pack(fill="x", padx=10, pady=(3, 10))
        tk.Label(row4, text="Комнат:", font=("Arial", 10), bg=COLOR_BG_PANEL, fg=COLOR_TEXT).pack(
            side="left"
        )
        self.rooms_combo = ttk.Combobox(
            row4,
            values=["Любое", "1", "2", "3", "4", "5+"],
            state="readonly",
            font=("Arial", 10),
            width=8,
        )
        self.rooms_combo.current(0)
        self.rooms_combo.pack(side="left", padx=(5, 20))
        tk.Label(row4, text="Этаж:", font=("Arial", 10), bg=COLOR_BG_PANEL, fg=COLOR_TEXT).pack(
            side="left"
        )
        self.floor_min = tk.Entry(
            row4, font=("Arial", 10), bd=0, relief="flat", bg="#FFFFFF", fg=COLOR_TEXT, width=5
        )
        self.floor_min.insert(0, "1")
        self.floor_min.pack(side="left", padx=(5, 5), ipady=4)
        tk.Label(row4, text="—", font=("Arial", 10), bg=COLOR_BG_PANEL, fg=COLOR_TEXT).pack(
            side="left"
        )
        self.floor_max = tk.Entry(
            row4, font=("Arial", 10), bd=0, relief="flat", bg="#FFFFFF", fg=COLOR_TEXT, width=5
        )
        self.floor_max.insert(0, "50")
        self.floor_max.pack(side="left", padx=(5, 0), ipady=4)

        # Кнопки
        btn_row = tk.Frame(self.card, bg=COLOR_BG_CARD)
        btn_row.pack(fill="x", padx=20, pady=(5, 10))

        tk.Button(
            btn_row,
            text="🔍  Найти",
            font=("Arial", 10, "bold"),
            bg=COLOR_BTN,
            fg=COLOR_TEXT,
            bd=0,
            relief="flat",
            padx=20,
            pady=5,
            cursor="hand2",
            command=self._on_search,
        ).pack(side="left")
        tk.Button(
            btn_row,
            text="○  Сбросить",
            font=("Arial", 10),
            bg=COLOR_BTN,
            fg=COLOR_TEXT,
            bd=0,
            relief="flat",
            padx=20,
            pady=5,
            cursor="hand2",
            command=self._on_reset,
        ).pack(side="left", padx=10)

        # Автопоиск
        for cb in (self.deal_combo, self.type_combo, self.district_combo, self.rooms_combo):
            cb.bind("<<ComboboxSelected>>", lambda e: self._on_search())
        self.card.bind_all("<Return>", lambda e: self._on_search())

    def _combo(self, parent, values):
        combo = ttk.Combobox(parent, values=values, state="readonly", font=("Arial", 10), width=14)
        combo.current(0)
        combo.pack(side="left", padx=(0, 8))
        return combo

    # ---------------- Сетка карточек ----------------

    def _build_cards_grid(self) -> None:
        canvas = tk.Canvas(self.card, bg=COLOR_BG_CARD, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.card, orient="vertical", command=canvas.yview)
        self.cards_container = tk.Frame(canvas, bg=COLOR_BG_CARD)

        self.cards_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=self.cards_container, anchor="nw", width=520)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 20))
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=(0, 20))
        canvas.bind_all(
            "<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units")
        )

        self.grid_frame = tk.Frame(self.cards_container, bg=COLOR_BG_CARD)
        self.grid_frame.pack(fill="both", expand=True)

        self.similar_title = tk.Label(
            self.cards_container,
            text="Похожие варианты",
            font=("Arial", 11, "bold"),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        )
        self.similar_frame = tk.Frame(self.cards_container, bg=COLOR_BG_CARD)

    def _make_card(self, parent, prop, index=0):
        card = tk.Frame(parent, bg=COLOR_CARD_ITEM)
        color = PHOTO_COLORS[index % len(PHOTO_COLORS)]

        photo = tk.Frame(card, bg=color, height=80)
        photo.pack(fill="x", padx=12, pady=(12, 8))
        photo.pack_propagate(False)
        tk.Label(
            photo,
            text=f"🏠\n{prop['property_type'].capitalize()}",
            font=("Arial", 10, "bold"),
            bg=color,
            fg="#FFFFFF",
            justify="center",
        ).pack(expand=True)

        price = prop["price"]
        price_text = (
            f"{price:,.0f} ₽/мес".replace(",", " ")
            if prop["deal_type"] == "аренда"
            else f"{price:,.0f} ₽".replace(",", " ")
        )
        tk.Label(
            card, text=price_text, font=("Arial", 11, "bold"), bg=COLOR_CARD_ITEM, fg=COLOR_TEXT
        ).pack(anchor="w", padx=12)

        rooms = prop.get("rooms") or 1
        type_label = (
            f"{rooms}-комн. кв."
            if prop["property_type"] == "квартира"
            else prop["property_type"].capitalize()
        )
        tk.Label(card, text=type_label, font=("Arial", 10), bg=COLOR_CARD_ITEM, fg=COLOR_TEXT).pack(
            anchor="w", padx=12
        )

        floor = prop.get("floor") or 1
        tk.Label(
            card,
            text=f"{prop['area']:.0f} м², {floor}/{prop['floors']}",
            font=("Arial", 10),
            bg=COLOR_CARD_ITEM,
            fg=COLOR_TEXT,
        ).pack(anchor="w", padx=12)

        tk.Label(
            card, text=prop["address"], font=("Arial", 10), bg=COLOR_CARD_ITEM, fg=COLOR_TEXT
        ).pack(anchor="w", padx=12)

        tk.Label(
            card, text=prop["district"], font=("Arial", 10), bg=COLOR_CARD_ITEM, fg=COLOR_TEXT
        ).pack(anchor="w", padx=12, pady=(0, 6))

        icons = tk.Frame(card, bg=COLOR_CARD_ITEM)
        icons.pack(anchor="w", padx=12, pady=(0, 12))
        tk.Label(icons, text="♥  💬", font=("Arial", 11), bg=COLOR_CARD_ITEM, fg=COLOR_TEXT).pack(
            side="left"
        )

        return card

    # ---------------- Поиск ----------------

    def _on_search(self) -> None:
        deal_map = {
            "Купить": "продажа",
            "Снять": "аренда",
            "Продажа": "продажа",
            "Аренда": "аренда",
        }
        type_map = {"Квартира": "квартира", "Дом": "дом", "Помещение": "помещение"}

        deal = deal_map.get(self.deal_combo.get())
        ptype = type_map.get(self.type_combo.get())
        district_name = self.district_combo.get()

        district_id = None
        if district_name and district_name != "Все районы":
            for d in self.property_service.get_districts():
                if d.name == district_name:
                    district_id = d.id
                    break

        results = self.search_service.search(
            deal_type=deal,
            property_type=ptype,
            district_id=district_id,
            min_area=parse_float(self.area_min.get()) or None,
            max_area=parse_float(self.area_max.get()) or None,
            min_price=parse_float(self.price_min.get()) or None,
            max_price=parse_float(self.price_max.get()) or None,
            min_floors=parse_int(self.floor_min.get()) or None,
            max_floors=parse_int(self.floor_max.get()) or None,
        )

        found_ids = {r["id"] for r in results}
        all_objects = self.search_service.search()
        similar = [o for o in all_objects if o["id"] not in found_ids]

        self._render(results, similar)

    def _on_reset(self) -> None:
        self.price_min.delete(0, "end")
        self.price_min.insert(0, "0")
        self.price_max.delete(0, "end")
        self.price_max.insert(0, "50000000")
        self.area_min.delete(0, "end")
        self.area_min.insert(0, "10")
        self.area_max.delete(0, "end")
        self.area_max.insert(0, "500")
        self.floor_min.delete(0, "end")
        self.floor_min.insert(0, "1")
        self.floor_max.delete(0, "end")
        self.floor_max.insert(0, "50")
        self.deal_combo.current(0)
        self.type_combo.current(0)
        self.district_combo.current(0)
        self.rooms_combo.current(0)
        self._on_search()

    def _render(self, rows: List[dict], similar: List[dict]) -> None:
        self.found_label.configure(text=f"Найдено {len(rows)} объектов")
        for w in self.grid_frame.winfo_children():
            w.destroy()
        for w in self.similar_frame.winfo_children():
            w.destroy()

        if rows:
            for i, prop in enumerate(rows):
                card = self._make_card(self.grid_frame, prop, index=i)
                card.grid(row=i // 2, column=i % 2, padx=8, pady=8, sticky="nsew")
        else:
            tk.Label(
                self.grid_frame,
                text="По вашим фильтрам ничего не найдено.\n" "Ниже — другие варианты.",
                font=("Arial", 10),
                bg=COLOR_BG_CARD,
                fg=COLOR_TEXT,
                justify="left",
            ).grid(row=0, column=0, columnspan=2, padx=8, pady=15, sticky="w")

        self.grid_frame.columnconfigure(0, weight=1)
        self.grid_frame.columnconfigure(1, weight=1)

        if similar:
            self.similar_title.pack(anchor="w", padx=8, pady=(20, 5))
            self.similar_frame.pack(fill="both", expand=True)
            for i, prop in enumerate(similar[:8]):
                card = self._make_card(self.similar_frame, prop, index=i + len(rows))
                card.grid(row=i // 2, column=i % 2, padx=8, pady=8, sticky="nsew")
            self.similar_frame.columnconfigure(0, weight=1)
            self.similar_frame.columnconfigure(1, weight=1)
        else:
            self.similar_title.pack_forget()
            self.similar_frame.pack_forget()
