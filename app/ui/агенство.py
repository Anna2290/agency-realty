"""Главное окно приложения (Tkinter) — MVC-контроллер верхнего уровня.

Оформление окон входа и регистрации соответствует макету из Figma.
После входа открывается главное окно с вкладками:
1. Главная страница (Dashboard) — статистика и последние объекты
2. Объекты — CRUD объектов недвижимости
3. Поиск — фильтрация
4. Коммерческие предложения — КП
"""

import tkinter as tk
from tkinter import ttk, messagebox

from app.config import APP_TITLE, WINDOW_SIZE
from app.logic.auth_service import AuthService
from app.ui.dashboard_view import DashboardView
from app.ui.property_view import PropertyView
from app.ui.search_view import SearchView
from app.ui.offer_view import OfferView


COLOR_BG_DARK = "#2C3E50"
COLOR_BG_MAIN = "#FFFFFF"
COLOR_BG_PANEL = "#B0B0B0"
COLOR_TEXT = "#000000"
COLOR_TEXT_GRAY = "#888888"
COLOR_BTN_BG = "#FFFFFF"
COLOR_BTN_TEXT = "#000000"


def safe_destroy(window: tk.Misc) -> None:
    """Безопасно закрывает окно (без ошибки при повторном вызове)."""
    try:
        if window.winfo_exists():
            window.destroy()
    except tk.TclError:
        pass


class BaseAuthDialog:
    """Базовый класс для окон входа и регистрации (общий дизайн)."""

    WIDTH = 560
    HEIGHT = 740
    CARD_WIDTH = 480
    CARD_HEIGHT = 680

    def __init__(self, parent: tk.Misc, title: str, subtitle: str) -> None:
        self.success = False
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.configure(bg=COLOR_BG_DARK)
        self.dialog.resizable(False, False)

        self.dialog.update_idletasks()
        sw = self.dialog.winfo_screenwidth()
        sh = self.dialog.winfo_screenheight()
        x = (sw - self.WIDTH) // 2
        y = (sh - self.HEIGHT) // 2
        self.dialog.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

        self.card = tk.Frame(self.dialog, bg=COLOR_BG_MAIN)
        self.card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=self.CARD_WIDTH,
            height=self.CARD_HEIGHT,
        )

        tk.Label(
            self.card,
            text="AGENCY ESTAT",
            font=("Arial", 18, "bold"),
            bg=COLOR_BG_MAIN,
            fg=COLOR_TEXT,
        ).pack(pady=(30, 5))

        tk.Label(
            self.card,
            text=subtitle,
            font=("Arial", 12),
            bg=COLOR_BG_MAIN,
            fg=COLOR_TEXT,
        ).pack(pady=(0, 20))

        self.panel = tk.Frame(self.card, bg=COLOR_BG_PANEL)
        self.panel.pack(padx=40, pady=10, fill="both", expand=True)

        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self) -> None:
        safe_destroy(self.dialog)

    def _make_label(self, parent: tk.Misc, text: str) -> tk.Label:
        return tk.Label(
            parent,
            text=text,
            font=("Arial", 11),
            bg=COLOR_BG_PANEL,
            fg=COLOR_TEXT,
            anchor="w",
        )

    def _make_entry(self, parent: tk.Misc, show: str = "") -> tk.Entry:
        return tk.Entry(
            parent,
            font=("Arial", 11),
            bd=0,
            relief="flat",
            bg="#FFFFFF",
            fg=COLOR_TEXT,
            show=show,
        )

    def _make_button(self, parent: tk.Misc, text: str, command) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            font=("Arial", 12),
            bg=COLOR_BTN_BG,
            fg=COLOR_BTN_TEXT,
            bd=0,
            relief="flat",
            activebackground="#E0E0E0",
            cursor="hand2",
            command=command,
        )


class LoginDialog(BaseAuthDialog):
    """Диалог входа в систему (по макету Figma)."""

    def __init__(self, parent: tk.Misc, auth: AuthService) -> None:
        super().__init__(parent, "Вход в систему", "Информационная система")
        self.auth = auth

        self._make_label(self.panel, "Логин").pack(anchor="w", padx=30, pady=(30, 5))
        self.login_entry = self._make_entry(self.panel)
        self.login_entry.pack(padx=30, pady=(0, 20), ipady=10, fill="x")
        self.login_entry.insert(0, "Введите логин")
        self.login_entry.configure(fg=COLOR_TEXT_GRAY)

        self._make_label(self.panel, "Пароль").pack(anchor="w", padx=30, pady=(10, 5))
        self.pass_entry = self._make_entry(self.panel, show="•")
        self.pass_entry.pack(padx=30, pady=(0, 30), ipady=10, fill="x")

        self._make_button(self.panel, "Войти", self._on_login).pack(
            padx=30, pady=(20, 30), ipady=10, fill="x"
        )

        links = tk.Frame(self.panel, bg=COLOR_BG_PANEL)
        links.pack(fill="x", padx=30, pady=(0, 20))

        tk.Label(
            links,
            text="Забыли пароль?",
            font=("Arial", 10),
            bg=COLOR_BG_PANEL,
            fg=COLOR_TEXT,
            cursor="hand2",
        ).pack(side="left")

        reg_link = tk.Label(
            links,
            text="Зарегистрироваться",
            font=("Arial", 10),
            bg=COLOR_BG_PANEL,
            fg=COLOR_TEXT,
            cursor="hand2",
        )
        reg_link.pack(side="right")
        reg_link.bind("<Button-1>", lambda e: self._open_register())

        self.login_entry.bind("<FocusIn>", self._clear_placeholder)
        self.login_entry.bind("<FocusOut>", self._restore_placeholder)
        self.pass_entry.bind("<Return>", lambda e: self._on_login())
        self.login_entry.bind("<Return>", lambda e: self.pass_entry.focus_set())

        try:
            self.dialog.grab_set()
        except tk.TclError:
            pass

        self.dialog.wait_window()

    def _clear_placeholder(self, _event) -> None:
        if self.login_entry.get() == "Введите логин":
            self.login_entry.delete(0, tk.END)
            self.login_entry.configure(fg=COLOR_TEXT)

    def _restore_placeholder(self, _event) -> None:
        if not self.login_entry.get():
            self.login_entry.insert(0, "Введите логин")
            self.login_entry.configure(fg=COLOR_TEXT_GRAY)

    def _on_login(self) -> None:
        username = self.login_entry.get()
        if username == "Введите логин":
            username = ""
        password = self.pass_entry.get()

        if self.auth.login(username, password):
            self.success = True
            safe_destroy(self.dialog)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")

    def _open_register(self) -> None:
        try:
            self.dialog.grab_release()
        except tk.TclError:
            pass
        RegisterDialog(self.dialog, self.auth, parent_login=self)
        if self.dialog.winfo_exists():
            try:
                self.dialog.grab_set()
                self.dialog.focus_force()
            except tk.TclError:
                pass


class RegisterDialog(BaseAuthDialog):
    """Диалог регистрации нового пользователя (по макету Figma)."""

    def __init__(
        self,
        parent: tk.Misc,
        auth: AuthService,
        parent_login: LoginDialog,
    ) -> None:
        super().__init__(parent, "Регистрация", "Регистрация")
        self.auth = auth
        self.parent_login = parent_login

        self._make_label(self.panel, "ФИО").pack(anchor="w", padx=30, pady=(20, 5))
        self.name_entry = self._make_entry(self.panel)
        self.name_entry.pack(padx=30, pady=(0, 15), ipady=8, fill="x")

        row1 = tk.Frame(self.panel, bg=COLOR_BG_PANEL)
        row1.pack(fill="x", padx=30, pady=(0, 10))

        left1 = tk.Frame(row1, bg=COLOR_BG_PANEL)
        left1.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self._make_label(left1, "Email").pack(anchor="w")
        self.email_entry = self._make_entry(left1)
        self.email_entry.pack(ipady=8, fill="x")

        right1 = tk.Frame(row1, bg=COLOR_BG_PANEL)
        right1.pack(side="right", fill="x", expand=True, padx=(5, 0))
        self._make_label(right1, "Логин").pack(anchor="w")
        self.login_entry = self._make_entry(right1)
        self.login_entry.pack(ipady=8, fill="x")

        row2 = tk.Frame(self.panel, bg=COLOR_BG_PANEL)
        row2.pack(fill="x", padx=30, pady=(0, 10))

        left2 = tk.Frame(row2, bg=COLOR_BG_PANEL)
        left2.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self._make_label(left2, "Пароль").pack(anchor="w")
        self.pass_entry = self._make_entry(left2, show="•")
        self.pass_entry.pack(ipady=8, fill="x")

        right2 = tk.Frame(row2, bg=COLOR_BG_PANEL)
        right2.pack(side="right", fill="x", expand=True, padx=(5, 0))
        self._make_label(right2, "Подтверждение").pack(anchor="w")
        self.pass2_entry = self._make_entry(right2, show="•")
        self.pass2_entry.pack(ipady=8, fill="x")

        self._make_label(self.panel, "Роль").pack(anchor="w", padx=30, pady=(5, 5))
        self.role_combo = ttk.Combobox(
            self.panel,
            values=["agent", "admin"],
            state="readonly",
            font=("Arial", 11),
        )
        self.role_combo.current(0)
        self.role_combo.pack(padx=30, pady=(0, 20), ipady=5, fill="x")

        self._make_button(self.panel, "ЗАРЕГИСТРИРОВАТЬСЯ", self._on_register).pack(
            padx=30, pady=(10, 20), ipady=10, fill="x"
        )

        link_frame = tk.Frame(self.panel, bg=COLOR_BG_PANEL)
        link_frame.pack(fill="x", padx=30, pady=(0, 20))

        back_link = tk.Label(
            link_frame,
            text="Уже есть аккаунт? Войти",
            font=("Arial", 10),
            bg=COLOR_BG_PANEL,
            fg=COLOR_TEXT,
            cursor="hand2",
        )
        back_link.pack()
        back_link.bind("<Button-1>", lambda e: self._back_to_login())

        try:
            self.dialog.grab_set()
        except tk.TclError:
            pass

        self.dialog.wait_window()

    def _on_close(self) -> None:
        safe_destroy(self.dialog)
        if self.parent_login.dialog.winfo_exists():
            try:
                self.parent_login.dialog.grab_set()
                self.parent_login.dialog.focus_force()
            except tk.TclError:
                pass

    def _on_register(self) -> None:
        full_name = self.name_entry.get().strip()
        username = self.login_entry.get().strip()
        password = self.pass_entry.get()
        password2 = self.pass2_entry.get()
        role = self.role_combo.get() or "agent"

        if not full_name:
            messagebox.showerror("Ошибка", "Введите ФИО.")
            return
        if not username:
            messagebox.showerror("Ошибка", "Введите логин.")
            return
        if not password:
            messagebox.showerror("Ошибка", "Введите пароль.")
            return
        if password != password2:
            messagebox.showerror("Ошибка", "Пароли не совпадают.")
            return

        user = self.auth.register(username, password, role=role)
        if user is None:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует.")
            return

        messagebox.showinfo(
            "Успех",
            f"Пользователь «{username}» зарегистрирован.\n" f"Теперь можно войти с этими данными.",
        )

        if self.parent_login.dialog.winfo_exists():
            self.parent_login.login_entry.delete(0, tk.END)
            self.parent_login.login_entry.insert(0, username)
            self.parent_login.login_entry.configure(fg=COLOR_TEXT)
            self.parent_login.pass_entry.focus_set()

        safe_destroy(self.dialog)
        if self.parent_login.dialog.winfo_exists():
            try:
                self.parent_login.dialog.grab_set()
                self.parent_login.dialog.focus_force()
            except tk.TclError:
                pass

    def _back_to_login(self) -> None:
        safe_destroy(self.dialog)
        if self.parent_login.dialog.winfo_exists():
            try:
                self.parent_login.dialog.grab_set()
                self.parent_login.dialog.focus_force()
            except tk.TclError:
                pass


class MainWindow:
    """Главное окно с вкладками: Главная / Объекты / Поиск / КП."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)

        self.auth = AuthService()

        login = LoginDialog(self.root, self.auth)
        if not login.success:
            safe_destroy(self.root)
            raise SystemExit("Вход отменён")

        # Основной Notebook с вкладками
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # 1. Dashboard
        self.dashboard_view = DashboardView(
            self.notebook,
            username=self.auth.current_user.username,
            on_add_property=self._go_to_property_add,
            on_open_search=self._go_to_search,
        )

        # 2. Объекты
        self.property_view = PropertyView(self.notebook)

        # 3. Поиск
        self.search_view = SearchView(self.notebook)

        # 4. Коммерческие предложения
        self.offer_view = OfferView(self.notebook)

        self.notebook.add(self.dashboard_view.frame, text="Главная")
        self.notebook.add(self.property_view.frame, text="Объекты")
        self.notebook.add(self.search_view.frame, text="Поиск")
        self.notebook.add(self.offer_view.frame, text="Коммерческие предложения")

        # Нижняя панель
        bottom = ttk.Frame(self.root)
        bottom.pack(fill="x")
        ttk.Label(
            bottom,
            text=f"Пользователь: {self.auth.current_user.username} "
            f"({self.auth.current_user.role})",
        ).pack(side="left", padx=10)
        ttk.Button(bottom, text="Выйти", command=self._on_logout).pack(
            side="right", padx=10, pady=5
        )

    def _go_to_property_add(self) -> None:
        """Переключает на вкладку «Объекты»."""
        self.notebook.select(self.property_view.frame)

    def _go_to_search(self) -> None:
        """Переключает на вкладку «Поиск»."""
        self.notebook.select(self.search_view.frame)

    def _on_logout(self) -> None:
        self.auth.logout()
        safe_destroy(self.root)

    def run(self) -> None:
        self.root.mainloop()
