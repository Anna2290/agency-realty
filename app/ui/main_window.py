"""Главное окно приложения (Tkinter).

Вкладки: Главная / Мои объекты / Подобрать.
Окна: Вход, Добавление объекта (Frame 6).
"""

import tkinter as tk
from tkinter import ttk, messagebox

from app.config import APP_TITLE, WINDOW_SIZE
from app.logic.auth_service import AuthService
from app.ui.dashboard_view import DashboardView
from app.ui.property_view import PropertyView
from app.ui.search_view import SearchView
from app.ui.add_property_view import AddPropertyView


COLOR_BG_DARK = "#2C3E50"
COLOR_BG_CARD = "#FFFFFF"
COLOR_BG_PANEL = "#B0B0B0"
COLOR_TEXT = "#000000"
COLOR_TEXT_GRAY = "#888888"
COLOR_BTN_BG = "#FFFFFF"
COLOR_BTN_TEXT = "#000000"


def safe_destroy(window: tk.Misc) -> None:
    try:
        if window.winfo_exists():
            window.destroy()
    except tk.TclError:
        pass


# ============================================================
#  ОКНО ВХОДА
# ============================================================


class LoginDialog:
    """Диалог входа в систему. Регистрация убрана."""

    WIDTH = 560
    HEIGHT = 740
    CARD_WIDTH = 480
    CARD_HEIGHT = 680

    def __init__(self, parent: tk.Misc, auth: AuthService) -> None:
        self.success = False
        self.parent = parent
        self.auth = auth

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Вход в систему")
        self.dialog.configure(bg=COLOR_BG_DARK)
        self.dialog.resizable(False, False)

        self.dialog.update_idletasks()
        sw = self.dialog.winfo_screenwidth()
        sh = self.dialog.winfo_screenheight()
        x = (sw - self.WIDTH) // 2
        y = (sh - self.HEIGHT) // 2
        self.dialog.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

        self.card = tk.Frame(self.dialog, bg=COLOR_BG_CARD)
        self.card.place(
            relx=0.5, rely=0.5, anchor="center", width=self.CARD_WIDTH, height=self.CARD_HEIGHT
        )

        tk.Label(
            self.card,
            text="AGENCY ESTAT",
            font=("Arial", 18, "bold"),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(pady=(30, 5))

        tk.Label(
            self.card,
            text="Информационная система",
            font=("Arial", 12),
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT,
        ).pack(pady=(0, 20))

        self.panel = tk.Frame(self.card, bg=COLOR_BG_PANEL)
        self.panel.pack(padx=40, pady=10, fill="both", expand=True)

        tk.Label(
            self.panel,
            text="Логин",
            font=("Arial", 11),
            bg=COLOR_BG_PANEL,
            fg=COLOR_TEXT,
            anchor="w",
        ).pack(anchor="w", padx=30, pady=(30, 5))

        self.login_entry = tk.Entry(
            self.panel, font=("Arial", 11), bd=0, relief="flat", bg="#FFFFFF", fg=COLOR_TEXT
        )
        self.login_entry.pack(padx=30, pady=(0, 20), ipady=10, fill="x")
        self.login_entry.insert(0, "Введите логин")
        self.login_entry.configure(fg=COLOR_TEXT_GRAY)

        tk.Label(
            self.panel,
            text="Пароль",
            font=("Arial", 11),
            bg=COLOR_BG_PANEL,
            fg=COLOR_TEXT,
            anchor="w",
        ).pack(anchor="w", padx=30, pady=(10, 5))

        self.pass_entry = tk.Entry(
            self.panel,
            font=("Arial", 11),
            bd=0,
            relief="flat",
            bg="#FFFFFF",
            fg=COLOR_TEXT,
            show="•",
        )
        self.pass_entry.pack(padx=30, pady=(0, 30), ipady=10, fill="x")

        tk.Button(
            self.panel,
            text="Войти",
            font=("Arial", 12),
            bg=COLOR_BTN_BG,
            fg=COLOR_BTN_TEXT,
            bd=0,
            relief="flat",
            activebackground="#E0E0E0",
            cursor="hand2",
            command=self._on_login,
        ).pack(padx=30, pady=(20, 30), ipady=10, fill="x")

        self.login_entry.bind("<FocusIn>", self._clear_placeholder)
        self.login_entry.bind("<FocusOut>", self._restore_placeholder)
        self.pass_entry.bind("<Return>", lambda e: self._on_login())
        self.login_entry.bind("<Return>", lambda e: self.pass_entry.focus_set())

        try:
            self.dialog.grab_set()
        except tk.TclError:
            pass

        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close)
        self.dialog.wait_window()

    def _on_close(self) -> None:
        safe_destroy(self.dialog)

    def _clear_placeholder(self, _event):
        if self.login_entry.get() == "Введите логин":
            self.login_entry.delete(0, tk.END)
            self.login_entry.configure(fg=COLOR_TEXT)

    def _restore_placeholder(self, _event):
        if not self.login_entry.get():
            self.login_entry.insert(0, "Введите логин")
            self.login_entry.configure(fg=COLOR_TEXT_GRAY)

    def _on_login(self):
        username = self.login_entry.get()
        if username == "Введите логин":
            username = ""
        password = self.pass_entry.get()
        if self.auth.login(username, password):
            self.success = True
            safe_destroy(self.dialog)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")


# ============================================================
#  ГЛАВНОЕ ОКНО
# ============================================================


class MainWindow:
    """Главное окно: Главная / Мои объекты / Подобрать."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.withdraw()

        self.auth = AuthService()

        login = LoginDialog(self.root, self.auth)
        if not login.success:
            safe_destroy(self.root)
            raise SystemExit("Вход отменён")

        self.root.deiconify()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # 1. Главная
        self.dashboard_view = DashboardView(
            self.notebook,
            username=getattr(self.auth.current_user, "username", "Менеджер"),
            on_add_property=self._open_add_property,
            on_open_search=self._go_to_search,
        )

        # 2. Мои объекты
        self.property_view = PropertyView(
            self.notebook,
            current_user=self.auth.current_user,
        )

        # 3. Подобрать — с рабочей кнопкой «Назад»
        self.search_view = SearchView(
            self.notebook,
            on_back=self._go_to_home,
        )

        self.notebook.add(self.dashboard_view.frame, text="Главная")
        self.notebook.add(self.property_view.frame, text="Мои объекты")
        self.notebook.add(self.search_view.frame, text="Подобрать")

        # Нижняя панель
        bottom = ttk.Frame(self.root)
        bottom.pack(fill="x")
        user_label = (
            f"Пользователь: {self.auth.current_user.username} " f"({self.auth.current_user.role})"
            if self.auth.current_user
            else "Пользователь: —"
        )
        ttk.Label(bottom, text=user_label).pack(side="left", padx=10)
        ttk.Button(bottom, text="Выйти", command=self._on_logout).pack(
            side="right", padx=10, pady=5
        )

    # ---------- Навигация ----------

    def _go_to_home(self) -> None:
        """Переключает на вкладку «Главная» (кнопка [ ← Назад ])."""
        self.notebook.select(self.dashboard_view.frame)

    def _go_to_search(self) -> None:
        """Переключает на вкладку «Подобрать»."""
        self.notebook.select(self.search_view.frame)

    # ---------- Добавление объекта ----------

    def _open_add_property(self) -> None:
        def _refresh() -> None:
            try:
                self.dashboard_view.refresh()
            except Exception:
                pass
            try:
                self.property_view._load_data()
            except Exception:
                pass
            try:
                self.search_view._on_search()
            except Exception:
                pass

        owner_id = self.auth.current_user.id if self.auth.current_user else None
        AddPropertyView(self.root, on_saved=_refresh, owner_id=owner_id)

    def _on_logout(self) -> None:
        self.auth.logout()
        safe_destroy(self.root)

    def run(self) -> None:
        try:
            self.root.lift()
            self.root.attributes("-topmost", True)
            self.root.after(1000, lambda: self.root.attributes("-topmost", False))
            self.root.focus_force()
        except tk.TclError:
            pass
        self.root.mainloop()
