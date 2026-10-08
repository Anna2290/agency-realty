"""Окно «Добавление объекта» — форма создания (Frame 6)."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Callable, Optional

from app.logic.property_service import PropertyService


COLOR_BG_DARK = "#2C3E50"
COLOR_BG_CARD = "#FFFFFF"
COLOR_BG_FIELD = "#B0B0B0"
COLOR_TEXT = "#000000"
COLOR_BORDER_BLUE = "#4A90E2"
COLOR_DIVIDER = "#E0E0E0"


class AddPropertyView:
    """Окно (Toplevel) «Добавление объекта» — Frame 6."""

    WINDOW_W = 400
    WINDOW_H = 820
    CARD_PAD = 12

    def __init__(
        self,
        parent: tk.Misc,
        on_saved: Optional[Callable] = None,
        owner_id: Optional[int] = None,
    ) -> None:
        self.service = PropertyService()
        self.on_saved = on_saved
        self.owner_id = owner_id
        self.photo_paths: list = []

        # Внешнее окно
        self.window = tk.Toplevel(parent)
        self.window.title("Добавление объекта")
        self.window.configure(bg=COLOR_BG_DARK)
        self.window.resizable(False, False)
        self.window.transient(parent)

        try:
            self.window.grab_set()
        except tk.TclError:
            pass

        self.window.update_idletasks()
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = (sw - self.WINDOW_W) // 2
        y = (sh - self.WINDOW_H) // 2
        self.window.geometry(f"{self.WINDOW_W}x{self.WINDOW_H}+{x}+{y}")

        # Белая карточка
        self.card = tk.Frame(self.window, bg=COLOR_BG_CARD)
        self.card.pack(
            fill="both",
            expand=True,
            padx=self.CARD_PAD,
            pady=self.CARD_PAD,
        )

        # Прокрутка
        canvas = tk.Canvas(self.card, bg=COLOR_BG_CARD, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.card, orient="vertical", command=canvas.yview)
        self.scrollable = tk.Frame(canvas, bg=COLOR_BG_CARD)

        self.scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=self.scrollable, anchor="nw", width=350)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"),
        )

        # Сборка интерфейса
        self._build_header()
        self._build_main_info()
        self._build_description()
        self._build_photos()
        self._build_status()
        self._build_footer()

    # -------- Шапка --------

    def _build_header(self) -> None:
        header = tk.Frame(self.scrollable, bg=COLOR_BG_CARD, height=36)
        header.pack(fill="x", padx=10, pady=(10, 5))
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🏢  Добавление объекта",
            font=("Arial", 10, "bold"),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(side="left")

        back = tk.Label(
            header,
            text="[ ← Назад ]",
            font=("Arial", 9),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
            cursor="hand2",
        )
        back.pack(side="right")
        back.bind("<Button-1>", lambda e: self._on_cancel())

        tk.Frame(self.scrollable, bg=COLOR_DIVIDER, height=1).pack(fill="x", padx=10, pady=(0, 10))

    # -------- Основная информация --------

    def _build_main_info(self) -> None:
        tk.Label(
            self.scrollable,
            text="ОСНОВНАЯ ИНФОРМАЦИЯ",
            font=("Arial", 9, "bold"),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(pady=(0, 12))

        body = tk.Frame(self.scrollable, bg=COLOR_BG_CARD)
        body.pack(fill="x", padx=15)

        # Ряд 1: Тип сделки | Тип недвижимости
        row1 = tk.Frame(body, bg=COLOR_BG_CARD)
        row1.pack(fill="x", pady=(0, 10))
        self.deal_combo = self._combo_field(row1, "Тип сделки", ["продажа", "аренда"])
        self.type_combo = self._combo_field(
            row1, "Тип недвижимости", ["квартира", "дом", "помещение"]
        )

        # Адрес (с синей рамкой)
        tk.Label(
            body,
            text="Адрес",
            font=("Arial", 9),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(anchor="w", pady=(0, 3))

        addr_frame = tk.Frame(body, bg=COLOR_BORDER_BLUE, bd=2)
        addr_frame.pack(fill="x", pady=(0, 12))

        self.address_entry = tk.Entry(
            addr_frame,
            font=("Arial", 10),
            bd=0,
            relief="flat",
            bg=COLOR_BG_FIELD,
            fg=COLOR_TEXT,
        )
        self.address_entry.pack(fill="x", ipady=7, padx=2, pady=2)

        # Ряд 2: Район | Площадь
        row2 = tk.Frame(body, bg=COLOR_BG_CARD)
        row2.pack(fill="x", pady=(0, 10))
        district_names = [d.name for d in self.service.get_districts()] or ["Центральный"]
        self.district_combo = self._combo_field(row2, "Район", district_names)
        self.area_entry = self._entry_field(row2, "Площадь, м²")

        # Ряд 3: Этаж | Этажность
        row3 = tk.Frame(body, bg=COLOR_BG_CARD)
        row3.pack(fill="x", pady=(0, 10))
        self.floor_entry = self._entry_field(row3, "Этаж")
        self.floors_entry = self._entry_field(row3, "Этажность")

        # Ряд 4: Комнат | Цена
        row4 = tk.Frame(body, bg=COLOR_BG_CARD)
        row4.pack(fill="x", pady=(0, 10))
        self.rooms_combo = self._combo_field(row4, "Кол-во комнат", ["1", "2", "3", "4", "5", "6+"])
        self.price_entry = self._entry_field(row4, "Цена")

    def _combo_field(self, parent, label, values):
        col = tk.Frame(parent, bg=COLOR_BG_CARD)
        col.pack(side="left", fill="x", expand=True, padx=(0, 6))
        tk.Label(
            col,
            text=label,
            font=("Arial", 9),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(anchor="w", pady=(0, 3))
        combo = ttk.Combobox(col, values=values, state="readonly", font=("Arial", 9))
        combo.pack(fill="x", ipady=3)
        if values:
            combo.current(0)
        return combo

    def _entry_field(self, parent, label):
        col = tk.Frame(parent, bg=COLOR_BG_CARD)
        col.pack(side="left", fill="x", expand=True, padx=(0, 6))
        tk.Label(
            col,
            text=label,
            font=("Arial", 9),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(anchor="w", pady=(0, 3))
        entry = tk.Entry(
            col,
            font=("Arial", 9),
            bd=0,
            relief="flat",
            bg=COLOR_BG_FIELD,
            fg=COLOR_TEXT,
        )
        entry.pack(fill="x", ipady=6)
        return entry

    # -------- Описание --------

    def _build_description(self) -> None:
        tk.Label(
            self.scrollable,
            text="ОПИСАНИЕ",
            font=("Arial", 9, "bold"),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(pady=(15, 6))

        self.desc_text = tk.Text(
            self.scrollable,
            height=4,
            font=("Arial", 9),
            bd=0,
            relief="flat",
            bg=COLOR_BG_FIELD,
            fg=COLOR_TEXT,
            wrap="word",
        )
        self.desc_text.pack(fill="x", padx=15, ipady=5)

    # -------- Фото --------

    def _build_photos(self) -> None:
        tk.Label(
            self.scrollable,
            text="ФОТОГРАФИИ",
            font=("Arial", 9, "bold"),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(pady=(15, 8))

        photos = tk.Frame(self.scrollable, bg=COLOR_BG_CARD)
        photos.pack()

        for _ in range(2):
            tk.Frame(photos, bg=COLOR_BG_FIELD, width=62, height=62).pack(side="left", padx=6)

        upload = tk.Frame(photos, bg=COLOR_BG_FIELD, width=62, height=62)
        upload.pack(side="left", padx=6)
        upload.pack_propagate(False)

        upload_label = tk.Label(
            upload,
            text="+\nЗагрузить",
            font=("Arial", 8),
            bg=COLOR_BG_FIELD,
            fg=COLOR_TEXT,
            justify="center",
            cursor="hand2",
        )
        upload_label.pack(expand=True, fill="both")
        upload_label.bind("<Button-1>", lambda e: self._on_upload_photo())

    def _on_upload_photo(self) -> None:
        paths = filedialog.askopenfilenames(
            title="Выберите фотографии",
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif")],
        )
        if paths:
            self.photo_paths.extend(paths)
            messagebox.showinfo("Фото добавлены", f"Выбрано файлов: {len(paths)}")

    # -------- Статус --------

    def _build_status(self) -> None:
        tk.Label(
            self.scrollable,
            text="Статус",
            font=("Arial", 9),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(anchor="w", padx=15, pady=(15, 3))

        self.status_combo = ttk.Combobox(
            self.scrollable,
            values=["активен", "архив", "продано", "сдано"],
            state="readonly",
            font=("Arial", 9),
        )
        self.status_combo.current(0)
        self.status_combo.pack(fill="x", padx=15, ipady=3)

    # -------- Футер --------

    def _build_footer(self) -> None:
        tk.Frame(self.scrollable, bg=COLOR_DIVIDER, height=1).pack(fill="x", padx=10, pady=(18, 0))

        footer = tk.Frame(self.scrollable, bg=COLOR_BG_CARD, height=40)
        footer.pack(fill="x", padx=10, pady=(8, 12))
        footer.pack_propagate(False)

        save = tk.Label(
            footer,
            text="[ 💾  Сохранить ]",
            font=("Arial", 10, "bold"),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
            cursor="hand2",
        )
        save.pack(side="left")
        save.bind("<Button-1>", lambda e: self._on_save())

        cancel = tk.Label(
            footer,
            text="[ ✕  Отмена ]",
            font=("Arial", 10),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
            cursor="hand2",
        )
        cancel.pack(side="right")
        cancel.bind("<Button-1>", lambda e: self._on_cancel())

    # -------- Логика --------

    def _on_save(self) -> None:
        address = self.address_entry.get().strip()
        if not address:
            messagebox.showerror("Ошибка", "Введите адрес.")
            return

        area_str = self.area_entry.get().strip()
        price_str = self.price_entry.get().strip()
        floors_str = self.floors_entry.get().strip()
        floor_str = self.floor_entry.get().strip()

        try:
            area = float(area_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Площадь должна быть числом.")
            return

        try:
            price = float(price_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Цена должна быть числом.")
            return

        try:
            floors = int(floors_str) if floors_str else 1
        except ValueError:
            messagebox.showerror("Ошибка", "Этажность должна быть целым числом.")
            return

        try:
            floor = int(floor_str) if floor_str else None
        except ValueError:
            floor = None

        rooms_str = self.rooms_combo.get()
        rooms = None
        if rooms_str:
            try:
                rooms = int(rooms_str.replace("+", ""))
            except ValueError:
                rooms = None

        district_name = self.district_combo.get()
        district = self.service.get_district_by_name(district_name)
        if district is None:
            messagebox.showerror("Ошибка", "Выберите район.")
            return

        property_type = self.type_combo.get() or "квартира"
        deal_type = self.deal_combo.get() or "продажа"
        title = f"{property_type.capitalize()}, {address}"
        description = self.desc_text.get("1.0", "end").strip()
        status = self.status_combo.get() or "активен"

        try:
            self.service.create(
                title=title,
                property_type=property_type,
                deal_type=deal_type,
                area=area,
                floors=floors,
                floor=floor,
                district_id=district.id,
                address=address,
                price=price,
                description=description,
                rooms=rooms,
                status=status,
                owner_id=self.owner_id,
            )
            messagebox.showinfo("Успех", "Объект сохранён.")
            if self.on_saved:
                self.on_saved()
            self._on_cancel()
        except Exception as exc:
            messagebox.showerror("Ошибка сохранения", str(exc))

    def _on_cancel(self) -> None:
        try:
            if self.window.winfo_exists():
                self.window.destroy()
        except tk.TclError:
            pass
        self.service.close()
