import io
import customtkinter as ctk
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from src.core import click_stats
from src.ui import theme

_PERIODS = {
    "Heure": "hour",
    "Jour": "day",
    "Semaine": "week",
    "Mois": "month",
    "Année": "year",
}

_W, _H = 640, 340


class AnalyticsWindow(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.withdraw()
        self.title("Analyses — Clics AutoClaude")
        self.geometry("720x520")
        self.resizable(False, False)
        self.configure(fg_color=theme.PALETTE["bg"])
        self._current_period = "hour"
        self._ctk_img = None
        self._img_label = None
        self._build_ui()
        self.after(100, self._show)

    def _show(self):
        self.deiconify()
        self.lift()
        self.focus_force()
        self.grab_set()
        self._draw(self._current_period)

    def _build_ui(self):
        ctk.CTkLabel(
            self,
            text="Analyse des clics",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=theme.PALETTE["text"],
        ).pack(pady=(16, 8))

        seg = ctk.CTkSegmentedButton(
            self,
            values=list(_PERIODS.keys()),
            command=self._on_period_change,
            font=ctk.CTkFont(family="Segoe UI", size=18),
            fg_color=theme.PALETTE["bg_secondary"],
            selected_color=theme.PALETTE["primary"],
            selected_hover_color=theme.PALETTE["primary"],
            unselected_color=theme.PALETTE["bg_secondary"],
            unselected_hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
        )
        seg.pack(pady=(0, 12))
        seg.set("Heure")

        frame = ctk.CTkFrame(self, fg_color=theme.PALETTE["bg_secondary"], corner_radius=10)
        frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self._img_label = ctk.CTkLabel(frame, text="Chargement…", text_color=theme.PALETTE["text_muted"])
        self._img_label.pack(fill="both", expand=True, padx=8, pady=8)

    def _on_period_change(self, label: str):
        self._current_period = _PERIODS[label]
        self._draw(self._current_period)

    def _draw(self, period: str):
        if self._img_label is None:
            return

        data = click_stats.aggregate(period)
        labels = [d[0] for d in data]
        values = [d[1] for d in data]

        bg = theme.PALETTE["bg_secondary"]
        primary = theme.PALETTE["primary"]
        text_color = theme.PALETTE["text"]
        muted = theme.PALETTE["text_muted"]

        dpi = 100
        fig, ax = plt.subplots(figsize=(_W / dpi, _H / dpi), dpi=dpi, facecolor=bg)
        ax.set_facecolor(bg)

        if values:
            bars = ax.bar(labels, values, color=primary, width=0.5, zorder=2)
            for bar in bars:
                h = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    h + 0.05,
                    str(int(h)),
                    ha="center", va="bottom",
                    color=text_color,
                    fontsize=9,
                )
        else:
            ax.text(
                0.5, 0.5, "Aucune donnée pour cette période",
                ha="center", va="center",
                transform=ax.transAxes,
                color=muted, fontsize=13,
            )

        ax.tick_params(colors=muted, labelsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(muted)
        ax.spines["bottom"].set_color(muted)
        ax.set_ylabel("Clics", color=muted, fontsize=10)
        ax.grid(axis="y", color=muted, alpha=0.2, zorder=1)
        fig.tight_layout(pad=1.5)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", facecolor=bg)
        plt.close(fig)
        buf.seek(0)
        pil_img = Image.open(buf).copy()
        buf.close()

        self._ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(_W, _H))
        self._img_label.configure(image=self._ctk_img, text="")
