"""Fenêtre d'analyse des clics avec navigation temporelle et stats."""

import io
import calendar
from datetime import datetime, timedelta

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

_W, _H = 660, 280


def _subtract_months(dt: datetime, n: int) -> datetime:
    month = dt.month - 1 - n
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


def _add_months(dt: datetime, n: int) -> datetime:
    return _subtract_months(dt, -n)


class AnalyticsWindow(ctk.CTkToplevel):
    """Fenêtre d'analyse avec navigation, mode récent/tout et bandeau stats."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.withdraw()
        self.title("Analyses — Clics AutoClaude")
        self.geometry("760x600")
        self.resizable(False, False)
        self.configure(fg_color=theme.PALETTE["bg"])

        self._current_period = "hour"
        self._mode = "recent"   # "recent" | "all"
        self._offset = 0        # 0 = période courante, 1 = précédente…
        self._ctk_img = None
        self._img_label = None

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._show)

    def _show(self):
        self.deiconify()
        self.lift()
        self.focus_force()
        self.grab_set()
        self._refresh()

    def _build_ui(self):
        ctk.CTkLabel(
            self,
            text="Analyse des clics",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=theme.PALETTE["text"],
        ).pack(pady=(14, 8))

        # Sélecteur période + toggle Récent/Tout
        top_row = ctk.CTkFrame(self, fg_color="transparent")
        top_row.pack(pady=(0, 6))

        self._seg = ctk.CTkSegmentedButton(
            top_row,
            values=list(_PERIODS.keys()),
            command=self._on_period_change,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=theme.PALETTE["bg_secondary"],
            selected_color=theme.PALETTE["primary"],
            selected_hover_color=theme.PALETTE["primary"],
            unselected_color=theme.PALETTE["bg_secondary"],
            unselected_hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
        )
        self._seg.pack(side="left", padx=(0, 12))
        self._seg.set("Heure")

        self._mode_seg = ctk.CTkSegmentedButton(
            top_row,
            values=["Récent", "Tout"],
            command=self._on_mode_change,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=theme.PALETTE["bg_secondary"],
            selected_color=theme.PALETTE["border"],
            selected_hover_color=theme.PALETTE["border"],
            unselected_color=theme.PALETTE["bg_secondary"],
            unselected_hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
            width=130,
        )
        self._mode_seg.pack(side="left")
        self._mode_seg.set("Récent")

        # Navigation (toujours présente, boutons désactivés en mode Récent)
        nav = ctk.CTkFrame(self, fg_color="transparent")
        nav.pack(pady=(0, 6))

        self._btn_prev = ctk.CTkButton(
            nav,
            text="‹ Précédent",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=theme.PALETTE["bg_secondary"],
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
            border_color=theme.PALETTE["border"],
            border_width=1,
            corner_radius=6,
            width=110,
            height=28,
            command=self._go_prev,
        )
        self._btn_prev.pack(side="left", padx=(0, 8))

        self._nav_label = ctk.CTkLabel(
            nav,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=theme.PALETTE["text_muted"],
            width=200,
            anchor="center",
        )
        self._nav_label.pack(side="left", padx=(0, 8))

        self._btn_next = ctk.CTkButton(
            nav,
            text="Suivant ›",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=theme.PALETTE["bg_secondary"],
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
            border_color=theme.PALETTE["border"],
            border_width=1,
            corner_radius=6,
            width=110,
            height=28,
            command=self._go_next,
        )
        self._btn_next.pack(side="left")

        # Bandeau stats
        stats_frame = ctk.CTkFrame(self, fg_color=theme.PALETTE["bg_secondary"], corner_radius=8)
        stats_frame.pack(fill="x", padx=20, pady=(0, 8))

        self._stat_labels = {}
        for i, (key, title) in enumerate([
            ("total",       "Total clics"),
            ("avg_per_day", "Moy / jour actif"),
            ("record",      "Record (1 jour)"),
            ("active_days", "Jours actifs"),
        ]):
            cell = ctk.CTkFrame(stats_frame, fg_color="transparent")
            cell.grid(row=0, column=i, padx=16, pady=8, sticky="nsew")
            stats_frame.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(
                cell,
                text=title,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=theme.PALETTE["text_muted"],
            ).pack()
            lbl = ctk.CTkLabel(
                cell,
                text="—",
                font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
                text_color=theme.PALETTE["primary"],
            )
            lbl.pack()
            self._stat_labels[key] = lbl

        # Graphique
        chart_frame = ctk.CTkFrame(self, fg_color=theme.PALETTE["bg_secondary"], corner_radius=10)
        chart_frame.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        self._img_label = ctk.CTkLabel(
            chart_frame, text="Chargement…", text_color=theme.PALETTE["text_muted"]
        )
        self._img_label.pack(fill="both", expand=True, padx=8, pady=8)

        # Bouton Fermer
        ctk.CTkButton(
            self,
            text="Fermer",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=theme.PALETTE["bg_secondary"],
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["warning"],
            border_color=theme.PALETTE["border"],
            border_width=1,
            corner_radius=8,
            width=120,
            height=32,
            command=self._on_close,
        ).pack(pady=(0, 12))

    # ── callbacks ──────────────────────────────────────────────────────────

    def _on_period_change(self, label: str):
        self._current_period = _PERIODS[label]
        self._offset = 0
        self._refresh()

    def _on_mode_change(self, value: str):
        self._mode = "recent" if value == "Récent" else "all"
        self._offset = 0
        self._refresh()

    def _go_prev(self):
        self._offset += 1
        self._refresh()

    def _go_next(self):
        if self._offset > 0:
            self._offset -= 1
            self._refresh()

    # ── logique de plage ───────────────────────────────────────────────────

    def _compute_range(self) -> tuple:
        """Retourne (start, end, label) selon mode/period/offset."""
        now = datetime.now().astimezone()
        p = self._current_period
        off = self._offset

        if self._mode == "recent":
            if p == "hour":
                return now - timedelta(hours=24), now, "Dernières 24h"
            elif p == "day":
                return now - timedelta(days=30), now, "30 derniers jours"
            elif p == "week":
                return now - timedelta(weeks=12), now, "12 dernières semaines"
            elif p == "month":
                return _subtract_months(now, 12), now, "12 derniers mois"
            else:
                return None, None, "Tout l'historique"

        # mode "all" — navigation par fenêtre
        if p == "hour":
            target = (now - timedelta(days=off)).date()
            start = datetime(target.year, target.month, target.day, tzinfo=now.tzinfo)
            return start, start + timedelta(days=1), target.strftime("%d %b %Y")
        elif p == "day":
            ref = _subtract_months(
                now.replace(day=1, hour=0, minute=0, second=0, microsecond=0), off
            )
            return ref, _add_months(ref, 1), ref.strftime("%B %Y").capitalize()
        elif p == "week":
            year = now.year - off
            start = datetime(year, 1, 1, tzinfo=now.tzinfo)
            return start, datetime(year + 1, 1, 1, tzinfo=now.tzinfo), str(year)
        elif p == "month":
            year = now.year - off
            start = datetime(year, 1, 1, tzinfo=now.tzinfo)
            return start, datetime(year + 1, 1, 1, tzinfo=now.tzinfo), str(year)
        else:
            return None, None, "Tout l'historique"

    # ── rafraîchissement ───────────────────────────────────────────────────

    def _refresh(self):
        start, end, label = self._compute_range()

        # Navigation — état des boutons
        is_year_all = (self._current_period == "year")
        nav_active = (self._mode == "all") and not is_year_all
        self._btn_prev.configure(state="normal" if nav_active else "disabled")
        self._btn_next.configure(state="normal" if (nav_active and self._offset > 0) else "disabled")
        self._nav_label.configure(text=label)

        events = click_stats.filter_events_range(start, end)

        stats = click_stats.get_stats_for_events(events)
        self._stat_labels["total"].configure(text=f"{stats['total']:,}".replace(",", " "))
        self._stat_labels["avg_per_day"].configure(text=str(stats["avg_per_day"]))
        self._stat_labels["record"].configure(text=str(stats["record"]))
        self._stat_labels["active_days"].configure(text=str(stats["active_days"]))

        self._draw(self._current_period, events)

    def _draw(self, period: str, events: list[str]):
        if self._img_label is None:
            return

        data = click_stats.aggregate_events(period, events)
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
            ax.bar(labels, values, color=primary, width=0.5, zorder=2)
            for bar in ax.patches:
                h = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    h + 0.05,
                    str(int(h)),
                    ha="center", va="bottom",
                    color=text_color, fontsize=9,
                )
            if len(labels) > 14:
                plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)
        else:
            ax.text(
                0.5, 0.5, "Aucune donnée pour cette période",
                ha="center", va="center",
                transform=ax.transAxes,
                color=muted, fontsize=13,
            )

        ax.tick_params(colors=muted, labelsize=9)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
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

    def _on_close(self):
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
