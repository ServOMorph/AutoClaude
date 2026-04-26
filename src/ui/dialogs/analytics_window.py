"""TODO: description du module."""

import io
import customtkinter as ctk
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from src.core import click_stats
from src.ui import theme

_WINDOWS = {
    "Aujourd'hui": "today",
    "7 jours":     "7d",
    "30 jours":    "30d",
    "12 mois":     "12m",
    "Tout":        "all",
}

_W, _H = 640, 300


class AnalyticsWindow(ctk.CTkToplevel):
    """TODO: description de AnalyticsWindow."""
    def __init__(self, master, **kwargs):
        """TODO: description de __init__."""
        super().__init__(master, **kwargs)
        self.withdraw()
        self.title("Analyses — Clics AutoClaude")
        self.geometry("720x580")
        self.resizable(False, False)
        self.configure(fg_color=theme.PALETTE["bg"])
        self._current_window = "today"
        self._ctk_img = None
        self._img_label = None
        self._stat_labels: dict[str, ctk.CTkLabel] = {}
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._show)

    def _show(self):
        """TODO: description de _show."""
        self.deiconify()
        self.lift()
        self.focus_force()
        self.grab_set()
        self._draw(self._current_window)

    def _build_ui(self):
        """TODO: description de _build_ui."""
        ctk.CTkLabel(
            self,
            text="Analyse des clics",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=theme.PALETTE["text"],
        ).pack(pady=(16, 8))

        seg = ctk.CTkSegmentedButton(
            self,
            values=list(_WINDOWS.keys()),
            command=self._on_window_change,
            font=ctk.CTkFont(family="Segoe UI", size=15),
            fg_color=theme.PALETTE["bg_secondary"],
            selected_color=theme.PALETTE["primary"],
            selected_hover_color=theme.PALETTE["primary"],
            unselected_color=theme.PALETTE["bg_secondary"],
            unselected_hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
        )
        seg.pack(pady=(0, 10))
        seg.set("Aujourd'hui")

        # Graphique
        chart_frame = ctk.CTkFrame(self, fg_color=theme.PALETTE["bg_secondary"], corner_radius=10)
        chart_frame.pack(fill="x", padx=20, pady=(0, 8))

        self._img_label = ctk.CTkLabel(chart_frame, text="Chargement…", text_color=theme.PALETTE["text_muted"])
        self._img_label.pack(fill="both", expand=True, padx=8, pady=8)

        # Bandeau de stats
        stats_frame = ctk.CTkFrame(self, fg_color=theme.PALETTE["bg_secondary"], corner_radius=10)
        stats_frame.pack(fill="x", padx=20, pady=(0, 16))

        stat_defs = [
            ("total",              "Total",         "—"),
            ("avg_per_active_day", "Moy/jour actif","—"),
            ("record",             "Record",        "—"),
            ("active_days",        "Jours actifs",  "—"),
        ]

        for key, label_text, default in stat_defs:
            col = ctk.CTkFrame(stats_frame, fg_color="transparent")
            col.pack(side="left", expand=True, fill="both", padx=4, pady=10)

            ctk.CTkLabel(
                col,
                text=label_text,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=theme.PALETTE["text_muted"],
            ).pack()

            val_lbl = ctk.CTkLabel(
                col,
                text=default,
                font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
                text_color=theme.PALETTE["primary"],
            )
            val_lbl.pack()
            self._stat_labels[key] = val_lbl

    def _on_window_change(self, label: str):
        """TODO: description de _on_window_change."""
        self._current_window = _WINDOWS[label]
        self._draw(self._current_window)

    def _draw(self, window: str):
        """TODO: description de _draw."""
        if self._img_label is None:
            return

        data, stats = click_stats.aggregate_windowed(window)
        labels = [d[0] for d in data]
        values = [d[1] for d in data]

        bg      = theme.PALETTE["bg_secondary"]
        primary = theme.PALETTE["primary"]
        text_c  = theme.PALETTE["text"]
        muted   = theme.PALETTE["text_muted"]

        max_val = max(values) if values else 1
        colors = [primary if v == max_val and v > 0 else primary + "99" for v in values]

        dpi = 100
        fig, ax = plt.subplots(figsize=(_W / dpi, _H / dpi), dpi=dpi, facecolor=bg)
        ax.set_facecolor(bg)

        if any(v > 0 for v in values):
            ax.bar(range(len(labels)), values, color=colors, width=0.6, zorder=2)
            ax.set_xticks(range(len(labels)))
            rotation = 30 if len(labels) > 10 else 0
            ax.set_xticklabels(labels, rotation=rotation, ha="right" if rotation else "center", fontsize=8)
            for i, v in enumerate(values):
                if v > 0:
                    ax.text(i, v + max_val * 0.01, str(v), ha="center", va="bottom",
                            color=text_c, fontsize=8)
        else:
            ax.text(0.5, 0.5, "Aucune donnée pour cette période",
                    ha="center", va="center", transform=ax.transAxes,
                    color=muted, fontsize=13)
            ax.set_xticks([])

        ax.tick_params(colors=muted, labelsize=8)
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

        # Mise à jour bandeau stats
        avg = stats["avg_per_active_day"]
        self._stat_labels["total"].configure(text=str(stats["total"]))
        self._stat_labels["avg_per_active_day"].configure(text=f"{avg:.1f}")
        self._stat_labels["record"].configure(text=str(stats["record"]))
        self._stat_labels["active_days"].configure(text=str(stats["active_days"]))

        ctk.CTkButton(
            self,
            text="Fermer",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            fg_color=theme.PALETTE["bg_secondary"],
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
            border_color=theme.PALETTE["border"],
            border_width=1,
            corner_radius=8,
            width=120,
            height=34,
            command=self._on_close,
        ).pack(pady=(0, 16))

    def _on_close(self):
        """Fermeture propre : libérer la figure courante et détruire la fenêtre."""
        plt.close("all")
        self._ctk_img = None
        if self._img_label:
            self._img_label.configure(image=None)
            self._img_label = None
        try:
            self.grab_release()
        except Exception:
            pass
        self.destroy()
