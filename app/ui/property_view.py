"""Вкладка «Мои объекты»."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from app.logic.property_service import PropertyService
from app.utils.validators import is_positive_number, is_positive_int
from app.ui.add_property_view import AddPropertyView


COLOR_BG_DARK = "#2C3E50"
COLOR_BG_CARD = "#FFFFFF"
COLOR_BG_FIELD = "#B0B0B0"
COLOR_TEXT = "#000000"
COLOR_BORDER = "#DDDDDD"
COLOR_BTN = "#E8E8E8"

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


class PropertyView:
    """Вкладка «Мои объекты» — CRUD только своих объектов."""

    def __init__(self, parent: ttk.Notebook, current_user=None) -> None:
        self.service = PropertyService()
        self.current_user = current_user
        self.selected_id: Optional[int] = None

        self.frame = tk.Frame(parent, bg=COLOR_BG_DARK)
        self.card = tk.Frame(self.frame, bg=COLOR_BG_CARD)
        self.card.pack(fill="both", expand=True, padx=25, pady=25)

        self._build_header()
        self._build_form()
        self._build_buttons()
        self._build_table()
        self._load_data()

    def _build_header(self) -> None:
        header = tk.Frame(self.card, bg=COLOR_BG_CARD, height=40)
        header.pack(fill="x", padx=20, pady=(15, 5))
        header.pack_propagate(False)
        name = getattr(self.current_user, "username", "—") if self.current_user else "—"
        tk.Label(
            header,
            text=f"🏢   Мои объекты — {name}",
            font=("Arial", 12, "bold"),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(side="left")
        tk.Frame(self.card, bg=COLOR_BORDER, height=1).pack(fill="x", padx=20, pady=(5, 15))

    def _build_form(self) -> None:
        form = tk.Frame(self.card, bg=COLOR_BG_CARD)
        form.pack(fill="x", padx=20, pady=(0, 10))

        row1 = tk.Frame(form, bg=COLOR_BG_CARD)
        row1.pack(fill="x", pady=4)
        self.deal_combo = self._combo_field(row1, "Тип сделки", ["продажа", "аренда"])
        self.type_combo = self._combo_field(
            row1, "Тип недвижимости", ["квартира", "дом", "помещение"]
        )

        row2 = tk.Frame(form, bg=COLOR_BG_CARD)
        row2.pack(fill="x", pady=4)
        self.address_entry = self._entry_field(row2, "Адрес")

        row3 = tk.Frame(form, bg=COLOR_BG_CARD)
        row3.pack(fill="x", pady=4)
        district_names = [d.name for d in self.service.get_districts()]
        self.district_combo = self._combo_field(row3, "Район", district_names)
        self.area_entry = self._entry_field(row3, "Площадь, м²")

        row4 = tk.Frame(form, bg=COLOR_BG_CARD)
        row4.pack(fill="x", pady=4)
        self.floor_entry = self._entry_field(row4, "Этаж")
        self.floors_entry = self._entry_field(row4, "Этажность")

        row5 = tk.Frame(form, bg=COLOR_BG_CARD)
        row5.pack(fill="x", pady=4)
        self.rooms_combo = self._combo_field(row5, "Кол-во комнат", ["1", "2", "3", "4", "5", "6+"])
        self.price_entry = self._entry_field(row5, "Цена, ₽")

    def _combo_field(self, parent, label, values):
        col = tk.Frame(parent, bg=COLOR_BG_CARD)
        col.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Label(col, text=label, font=("Arial", 10), bg=COLOR_BG_CARD, fg=COLOR_TEXT).pack(
            anchor="w", pady=(0, 3)
        )
        combo = ttk.Combobox(col, values=values, state="readonly", font=("Arial", 10))
        combo.pack(fill="x", ipady=3)
        if values:
            combo.current(0)
        return combo

    def _entry_field(self, parent, label):
        col = tk.Frame(parent, bg=COLOR_BG_CARD)
        col.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Label(col, text=label, font=("Arial", 10), bg=COLOR_BG_CARD, fg=COLOR_TEXT).pack(
            anchor="w", pady=(0, 3)
        )
        entry = tk.Entry(
            col, font=("Arial", 10), bd=0, relief="flat", bg=COLOR_BG_FIELD, fg=COLOR_TEXT
        )
        entry.pack(fill="x", ipady=6)
        return entry

    def _build_buttons(self) -> None:
        btns = tk.Frame(self.card, bg=COLOR_BG_CARD)
        btns.pack(fill="x", padx=20, pady=(5, 15))
        tk.Button(
            btns,
            text="+  Добавить",
            font=("Arial", 10, "bold"),
            bg=COLOR_BTN,
            fg=COLOR_TEXT,
            bd=0,
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._on_create_via_dialog,
        ).pack(side="left")
        tk.Button(
            btns,
            text="✎  Обновить",
            font=("Arial", 10),
            bg=COLOR_BTN,
            fg=COLOR_TEXT,
            bd=0,
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._on_update,
        ).pack(side="left", padx=8)
        tk.Button(
            btns,
            text="✕  Удалить",
            font=("Arial", 10),
            bg=COLOR_BTN,
            fg=COLOR_TEXT,
            bd=0,
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._on_delete,
        ).pack(side="left", padx=8)
        tk.Button(
            btns,
            text="○  Очистить",
            font=("Arial", 10),
            bg=COLOR_BTN,
            fg=COLOR_TEXT,
            bd=0,
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._on_clear,
        ).pack(side="left", padx=8)

    def _build_table(self) -> None:
        table_frame = tk.Frame(self.card, bg=COLOR_BG_CARD)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        columns = [
            ("photo", "Фото", 60),
            ("id", "ID", 40),
            ("type", "Тип", 90),
            ("deal", "Сделка", 80),
            ("rooms", "Комнат", 60),
            ("area", "Площадь", 70),
            ("floor", "Этаж", 60),
            ("price", "Цена", 110),
            ("district", "Район", 110),
            ("address", "Адрес", 200),
        ]
        style = ttk.Style()
        style.configure("MyProp.Treeview", font=("Arial", 10), rowheight=44)
        style.configure("MyProp.Treeview.Heading", font=("Arial", 10, "bold"))
        self.tree = ttk.Treeview(
            table_frame,
            columns=[c[0] for c in columns],
            show="headings",
            style="MyProp.Treeview",
            height=10,
        )
        for col_id, col_title, width in columns:
            self.tree.heading(col_id, text=col_title)
            self.tree.column(col_id, width=width, anchor="center")
        self.tree.pack(fill="both", expand=True, side="left")
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _load_data(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        if not self.current_user:
            return
        props = self.service.get_by_owner(self.current_user.id)
        for i, p in enumerate(props):
            district_name = p.district.name if p.district else "—"
            rooms = p.rooms or 1
            floor = p.floor or 1
            photo_tag = f"photo_{i % len(PHOTO_COLORS)}"
            self.tree.tag_configure(photo_tag, background=PHOTO_COLORS[i % len(PHOTO_COLORS)])
            self.tree.insert(
                "",
                "end",
                iid=str(p.id),
                values=(
                    "🏠",
                    p.id,
                    p.property_type,
                    p.deal_type,
                    rooms,
                    f"{p.area:.0f}",
                    f"{floor}/{p.floors}",
                    f"{p.price:,.0f}".replace(",", " "),
                    district_name,
                    p.address,
                ),
                tags=(photo_tag,),
            )

    def _on_select(self, _event) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        prop = self.service.get_by_id(int(selection[0]))
        if not prop:
            return
        self.selected_id = prop.id
        self._fill_form(prop)

    def _fill_form(self, prop) -> None:
        if prop.deal_type in ["продажа", "аренда"]:
            self.deal_combo.current(["продажа", "аренда"].index(prop.deal_type))
        types = ["квартира", "дом", "помещение"]
        if prop.property_type in types:
            self.type_combo.current(types.index(prop.property_type))
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, prop.address or "")
        districts = [d.name for d in self.service.get_districts()]
        if prop.district and prop.district.name in districts:
            self.district_combo.current(districts.index(prop.district.name))
        self.area_entry.delete(0, tk.END)
        self.area_entry.insert(0, str(prop.area))
        self.floor_entry.delete(0, tk.END)
        self.floor_entry.insert(0, str(prop.floor or ""))
        self.floors_entry.delete(0, tk.END)
        self.floors_entry.insert(0, str(prop.floors))
        rooms_val = str(prop.rooms or 1)
        rooms_list = ["1", "2", "3", "4", "5", "6+"]
        if rooms_val in rooms_list:
            self.rooms_combo.current(rooms_list.index(rooms_val))
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, str(prop.price))

    def _validate_form(self) -> bool:
        if not self.address_entry.get().strip():
            messagebox.showerror("Ошибка", "Введите адрес.")
            return False
        if not is_positive_number(self.area_entry.get()):
            messagebox.showerror("Ошибка", "Площадь — число.")
            return False
        if not is_positive_int(self.floors_entry.get()):
            messagebox.showerror("Ошибка", "Этажность — число.")
            return False
        if not is_positive_number(self.price_entry.get()):
            messagebox.showerror("Ошибка", "Цена — число.")
            return False
        return True

    def _get_district_id(self):
        name = self.district_combo.get()
        for d in self.service.get_districts():
            if d.name == name:
                return d.id
        return None

    def _on_create_via_dialog(self) -> None:
        def _refresh():
            self._load_data()

        owner_id = self.current_user.id if self.current_user else None
        AddPropertyView(self.frame.winfo_toplevel(), on_saved=_refresh, owner_id=owner_id)

    def _on_update(self) -> None:
        if self.selected_id is None:
            messagebox.showwarning("Внимание", "Выберите объект.")
            return
        if not self._validate_form():
            return
        district_id = self._get_district_id()
        if district_id is None:
            messagebox.showerror("Ошибка", "Выберите район.")
            return
        try:
            rooms = int(self.rooms_combo.get().replace("+", ""))
        except ValueError:
            rooms = None
        self.service.update(
            self.selected_id,
            property_type=self.type_combo.get(),
            deal_type=self.deal_combo.get(),
            area=float(self.area_entry.get()),
            floors=int(self.floors_entry.get()),
            floor=int(self.floor_entry.get()) if self.floor_entry.get() else None,
            rooms=rooms,
            district_id=district_id,
            address=self.address_entry.get(),
            price=float(self.price_entry.get()),
        )
        self._load_data()
        messagebox.showinfo("Успех", "Объект обновлён.")

    def _on_delete(self) -> None:
        if self.selected_id is None:
            messagebox.showwarning("Внимание", "Выберите объект.")
            return
        if not messagebox.askyesno("Подтверждение", "Удалить?"):
            return
        self.service.delete(self.selected_id)
        self._load_data()
        self._on_clear()

    def _on_clear(self) -> None:
        self.selected_id = None
        self.address_entry.delete(0, tk.END)
        self.area_entry.delete(0, tk.END)
        self.floor_entry.delete(0, tk.END)
        self.floors_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.deal_combo.current(0)
        self.type_combo.current(0)
        self.district_combo.current(0)
        self.rooms_combo.current(0)
