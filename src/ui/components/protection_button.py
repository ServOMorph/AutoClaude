import customtkinter as ctk
from src.security.claude_md_protector import ClaudeMdProtector
from src.ui import theme


class ProtectionButton(ctk.CTkFrame):
    def __init__(self, master, project_path: str = "", button_width: int = 200, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._project_path = project_path

        self._btn = ctk.CTkButton(
            self,
            text="🛡  Protéger ce projet",
            font=ctk.CTkFont(family=theme._font(), size=18, weight="bold"),
            fg_color=theme.PALETTE["bg_secondary"],
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
            border_color=theme.PALETTE["border"],
            border_width=1,
            corner_radius=8,
            width=button_width,
            height=38,
            command=self._apply,
        )
        self._btn.pack()

        self._remove_btn = ctk.CTkButton(
            self,
            text="🗑  Retirer la protection",
            font=ctk.CTkFont(family=theme._font(), size=18, weight="bold"),
            fg_color="transparent",
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text_muted"],
            border_color=theme.PALETTE["border"],
            border_width=1,
            corner_radius=8,
            width=button_width,
            height=38,
            command=self._remove,
        )
        self._remove_btn.pack(pady=(4, 0))

        self._status = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=12),
            text_color=theme.PALETTE["text_muted"],
            wraplength=360,
            justify="center",
        )
        self._status.pack(pady=(4, 0))

    def set_project_path(self, path: str):
        self._project_path = path
        self._status.configure(text="")

    def _apply(self):
        if not self._project_path:
            self._status.configure(text="⚠ Aucun dossier sélectionné.", text_color=theme.PALETTE["warning"])
            return
        protector = ClaudeMdProtector(self._project_path)
        ok, msg = protector.apply()
        color = theme.PALETTE["success"] if ok else theme.PALETTE["warning"]
        self._status.configure(text=msg, text_color=color)

    def _remove(self):
        if not self._project_path:
            self._status.configure(text="⚠ Aucun dossier sélectionné.", text_color=theme.PALETTE["warning"])
            return
        protector = ClaudeMdProtector(self._project_path)
        ok, msg = protector.remove_protection()
        color = theme.PALETTE["success"] if ok else theme.PALETTE["warning"]
        self._status.configure(text=msg, text_color=color)
