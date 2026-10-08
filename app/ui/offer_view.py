"""Вкладка «Коммерческие предложения» (стиль Frame 5)."""

import tkinter as tk
from tkinter import ttk, messagebox

from app.logic.client_service import ClientService
from app.logic.offer_service import OfferService
from app.logic.property_service import PropertyService
from app.utils.pdf_exporter import export_offer_to_pdf


COLOR_BG_DARK = "#2C3E50"
COLOR_BG_CARD = "#FFFFFF"
COLOR_BG_FIELD = "#B0B0B0"
COLOR_TEXT = "#000000"
COLOR_BORDER = "#DDDDDD"


class OfferView:
    """Формирование КП (Frame 5)."""

    def __init__(self, parent: ttk.Notebook) -> None:
        self.client_service = ClientService()
        self.offer_service = OfferService()
        self.property_service = PropertyService()

        self._clients = []
        self._properties = []

        self.frame = tk.Frame(parent, bg=COLOR_BG_DARK)

        self.card = tk.Frame(self.frame, bg=COLOR_BG_CARD)
        self.card.pack(fill="both", expand=True, padx=25, pady=25)

        self._build_header()
        self._build_form()
        self._build_table()
        self._build_footer()

        self._load_clients()
        self._load_properties()
        self._load_offers()

    def _build_header(self) -> None:
        header = tk.Frame(self.card, bg=COLOR_BG_CARD, height=40)
        header.pack(fill="x", padx=30, pady=(20, 5))
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📄   Коммерческие предложения",
            font=("Arial", 11, "bold"),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(side="left")

        tk.Frame(self.card, bg=COLOR_BORDER, height=1).pack(fill="x", padx=30, pady=(5, 15))

    def _build_form(self) -> None:
        form = tk.Frame(self.card, bg=COLOR_BG_CARD)
        form.pack(fill="x", padx=30, pady=(0, 10))

        # Клиент
        tk.Label(
            form,
            text="Клиент:",
            font=("Arial", 10),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).grid(row=0, column=0, sticky="w", pady=4)
        self.client_combo = ttk.Combobox(form, width=40, state="readonly")
        self.client_combo.grid(row=0, column=1, padx=10, pady=4)

        # Объект
        tk.Label(
            form,
            text="Объект:",
            font=("Arial", 10),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).grid(row=1, column=0, sticky="w", pady=4)
        self.property_combo = ttk.Combobox(form, width=55, state="readonly")
        self.property_combo.grid(row=1, column=1, padx=10, pady=4)

        # Комментарий
        tk.Label(
            form,
            text="Комментарий:",
            font=("Arial", 10),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).grid(row=2, column=0, sticky="w", pady=4)
        self.comment_entry = tk.Entry(
            form,
            font=("Arial", 10),
            bd=0,
            relief="flat",
            bg=COLOR_BG_FIELD,
            fg=COLOR_TEXT,
        )
        self.comment_entry.grid(row=2, column=1, padx=10, pady=4, ipady=6, sticky="ew")

    def _build_table(self) -> None:
        table_frame = tk.Frame(self.card, bg=COLOR_BG_CARD)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(10, 10))

        columns = [
            ("id", "ID", 50),
            ("client", "Клиент", 200),
            ("property", "Объект", 280),
            ("comment", "Комментарий", 220),
            ("date", "Дата", 150),
        ]
        style = ttk.Style()
        style.configure("Frame5Off.Treeview", font=("Arial", 11), rowheight=26)
        style.configure("Frame5Off.Treeview.Heading", font=("Arial", 11))

        self.tree = ttk.Treeview(
            table_frame,
            columns=[c[0] for c in columns],
            show="headings",
            style="Frame5Off.Treeview",
            height=7,
        )
        for col_id, col_title, width in columns:
            self.tree.heading(col_id, text=col_title)
            self.tree.column(col_id, width=width, anchor="center")
        self.tree.pack(fill="both", expand=True)

    def _build_footer(self) -> None:
        tk.Frame(self.card, bg=COLOR_BORDER, height=1).pack(fill="x", padx=30, pady=(15, 0))

        footer = tk.Frame(self.card, bg=COLOR_BG_CARD, height=50)
        footer.pack(fill="x", padx=30, pady=(10, 20))

        tk.Label(
            footer,
            text="[ ✎  Сформировать КП ]",
            font=("Arial", 11),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
            cursor="hand2",
        ).pack(side="left")
        footer.winfo_children()[0].bind("<Button-1>", lambda e: self._on_create_offer())

        tk.Label(
            footer,
            text="[ ⬇  Экспорт в PDF ]",
            font=("Arial", 11),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
            cursor="hand2",
        ).pack(side="left", padx=15)
        footer.winfo_children()[1].bind("<Button-1>", lambda e: self._on_export_pdf())

        tk.Label(
            footer,
            text="[ ↻  Обновить ]",
            font=("Arial", 11),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
            cursor="hand2",
        ).pack(side="right")
        footer.winfo_children()[2].bind("<Button-1>", lambda e: self._on_refresh())

    def _load_clients(self) -> None:
        self._clients = self.client_service.get_all()
        self.client_combo["values"] = [f"{c.id} — {c.full_name}" for c in self._clients]

    def _load_properties(self) -> None:
        self._properties = self.property_service.get_all()
        self.property_combo["values"] = [f"{p.id} — {p.title}" for p in self._properties]

    def _load_offers(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        for offer in self.offer_service.get_all():
            self.tree.insert(
                "",
                "end",
                iid=str(offer["id"]),
                values=(
                    offer["id"],
                    offer["client"],
                    offer["property"],
                    offer["comment"],
                    offer["date"],
                ),
            )

    def _get_selected_client_id(self):
        value = self.client_combo.get()
        return int(value.split(" — ")[0]) if value else None

    def _get_selected_property_id(self):
        value = self.property_combo.get()
        return int(value.split(" — ")[0]) if value else None

    def _on_create_offer(self) -> None:
        cid = self._get_selected_client_id()
        pid = self._get_selected_property_id()
        if not cid or not pid:
            messagebox.showwarning("Внимание", "Выберите клиента и объект.")
            return
        self.offer_service.create(client_id=cid, property_id=pid, comment=self.comment_entry.get())
        self._load_offers()
        self.comment_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Коммерческое предложение сформировано.")

    def _on_export_pdf(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите КП в таблице.")
            return
        offer_id = int(selection[0])
        offers = [o for o in self.offer_service.get_all() if o["id"] == offer_id]
        if not offers:
            return
        offer = offers[0]
        client_data = type(
            "Client", (), {"full_name": offer["client"], "phone": "—", "email": "—"}
        )()
        prop_data = type(
            "Property",
            (),
            {"title": offer["property"], "property_type": "—", "area": 0, "floors": 0, "price": 0},
        )()
        filename = f"offer_{offer_id}.pdf"
        try:
            path = export_offer_to_pdf(client_data, [prop_data], filename)
            messagebox.showinfo("Готово", f"PDF сохранён: {path}")
        except Exception as exc:
            messagebox.showerror("Ошибка экспорта", str(exc))

    def _on_refresh(self) -> None:
        self._load_clients()
        self._load_properties()
        self._load_offers()
