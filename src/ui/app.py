import customtkinter as ctk
from src.config.constants import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, ASSET_LOGO_ICO, ASSET_YES_PNG
from src.config import settings
from src.core.autoclick_service import AutoclickService
from src.ui import theme
from src.ui.components.header import Header
from src.ui.components.warning_banner import WarningBanner
from src.ui.components.activate_button import ActivateButton
from src.ui.components.protection_button import ProtectionButton
from src.ui.components.footer import Footer
from src.ui.dialogs.folder_picker import pick_folder


class AutoClaudeApp(ctk.CTk):
    def __init__(self):
        theme.apply()
        super().__init__()

        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.configure(fg_color=theme.PALETTE["bg"])

        self.update_idletasks()
        x = (self.winfo_screenwidth() - WINDOW_WIDTH) // 2
        y = (self.winfo_screenheight() - WINDOW_HEIGHT) // 2
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        try:
            self.iconbitmap(str(ASSET_LOGO_ICO))
        except Exception:
            pass

        self._service: AutoclickService | None = None
        self._project_path: str = ""

        self._build_ui()
        self.bind("<Escape>", lambda _: self._stop_service())
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        Header(self).pack(fill="x", padx=20, pady=(20, 12))

        WarningBanner(
            self,
            text=(
                "• AutoClaude clique automatiquement sur les YES de ClaudeCode (VSCode)\n\n"
                "• ⚠️ À utiliser avec beaucoup de prudence — augmente l'autonomie de ClaudeCode\n\n"
                "• 🔒 Sécurité : protégez votre projet en le sélectionnant et en cliquant "
                "\"Protéger\" — restrictions périmètre injectées automatiquement dans .claude/CLAUDE.md du projet"
            ),
        ).pack(fill="x", padx=20, pady=(0, 16))

        self._activate_btn = ActivateButton(self, on_toggle=self._on_toggle)
        self._activate_btn.pack(pady=(0, 12))

        ctk.CTkButton(
            self,
            text="📁  Choisir dossier projet",
            font=theme.font_body(),
            fg_color=theme.PALETTE["bg_secondary"],
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
            border_color=theme.PALETTE["border"],
            border_width=1,
            corner_radius=8,
            width=360,
            height=38,
            command=self._pick_folder,
        ).pack(pady=(0, 4))

        self._folder_label = ctk.CTkLabel(
            self, text="Aucun dossier sélectionné",
            font=ctk.CTkFont(size=12),
            text_color=theme.PALETTE["text_muted"],
            wraplength=360,
        )
        self._folder_label.pack(pady=(0, 12))

        self._protection_btn = ProtectionButton(self, button_width=360)
        self._protection_btn.pack(pady=(0, 16))

        Footer(self).pack(fill="x", padx=20, pady=(0, 20), side="bottom")

    def _on_toggle(self, active: bool):
        if active:
            self._start_service()
        else:
            self._stop_service()

    def _start_service(self):
        image_path = str(ASSET_YES_PNG)
        interval = settings.get("interval")
        auto_stop = settings.get("auto_stop")
        self._service = AutoclickService(
            image_path=image_path,
            interval=interval,
            auto_stop=auto_stop,
            on_stop=self._on_service_stopped,
        )
        self._service.start()

    def _stop_service(self):
        if self._service:
            self._service.stop()
            self._service = None
        self._activate_btn.set_active(False)

    def _on_service_stopped(self):
        self.after(0, lambda: self._activate_btn.set_active(False))

    def _pick_folder(self):
        path = pick_folder()
        if path:
            self._project_path = path
            self._folder_label.configure(text=path)
            self._protection_btn.set_project_path(path)

    def _on_close(self):
        self._stop_service()
        self.destroy()
