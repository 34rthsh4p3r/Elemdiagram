import os
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def tisztit_oszlopnev(oszlopnev):
    """Oszlopnevek tisztítása."""
    if pd.isna(oszlopnev):
        return ""
    return str(oszlopnev).strip()


def adatok_beolvasasa(fajlnev, munkalap=0):
    """
    Excel beolvasása.

    Az első oszlop a mintaszám.
    Az összes további oszlop az Excel fejlécéből vett ábrázolandó elem.
    """
    df = pd.read_excel(fajlnev, sheet_name=munkalap, header=0)

    if df.shape[1] < 2:
        raise ValueError(
            "Az Excel fájlnak legalább két oszlopot kell tartalmaznia: "
            "mintaszám + legalább egy elem."
        )

    df.columns = [tisztit_oszlopnev(col) for col in df.columns]

    mintaszam_oszlop = df.columns[0]

    elemek = []
    for col in df.columns[1:]:
        col_szoveg = str(col).strip()

        if col_szoveg == "":
            continue

        if col_szoveg.lower().startswith("unnamed"):
            continue

        elemek.append(col_szoveg)

    if len(elemek) == 0:
        raise ValueError("Nem található ábrázolható elem-oszlop az Excel fejlécében.")

    df = df[[mintaszam_oszlop] + elemek].copy()

    for elem in elemek:
        df[elem] = (
            df[elem]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.strip()
        )

        df[elem] = pd.to_numeric(df[elem], errors="coerce")

    # Logaritmikus skálán csak pozitív érték ábrázolható
    df[elemek] = df[elemek].where(df[elemek] > 0, np.nan)

    return df, mintaszam_oszlop, elemek


class ElemDiagramApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Elemkoncentráció diagram")
        self.root.geometry("1400x800")

        self.aktualis_fajl = None

        self.figure = Figure(figsize=(20, 9), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.menu_letrehozasa()

        self.root.after(200, lambda: self.uj_fajl_kivalasztasa(indulaskor=True))

    def menu_letrehozasa(self):
        menubar = tk.Menu(self.root)

        fajl_menu = tk.Menu(menubar, tearoff=0)
        fajl_menu.add_command(
            label="Új fájl kiválasztása",
            command=self.uj_fajl_kivalasztasa
        )
        fajl_menu.add_command(
            label="Diagram mentése",
            command=self.abra_mentese_kezzel
        )
        fajl_menu.add_separator()
        fajl_menu.add_command(
            label="Kilépés",
            command=self.root.destroy
        )

        menubar.add_cascade(label="Fájl", menu=fajl_menu)

        self.root.config(menu=menubar)

    def fajl_kivalasztasa(self):
        fajlnev = filedialog.askopenfilename(
            parent=self.root,
            title="Válaszd ki az Excel fájlt",
            filetypes=[
                ("Excel fájlok", "*.xls *.xlsx"),
                ("Minden fájl", "*.*")
            ]
        )

        return fajlnev

    def uj_fajl_kivalasztasa(self, indulaskor=False):
        fajlnev = self.fajl_kivalasztasa()

        if not fajlnev:
            if indulaskor:
                self.root.destroy()
            return

        try:
            self.aktualis_fajl = fajlnev
            self.abra_frissitese(fajlnev)
        except Exception as e:
            messagebox.showerror(
                "Hiba",
                f"A fájl feldolgozása nem sikerült:\n\n{e}",
                parent=self.root
            )

            if indulaskor:
                self.root.destroy()

    def abra_frissitese(self, fajlnev):
        df, mintaszam_oszlop, elemek = adatok_beolvasasa(fajlnev)

        self.ax.clear()

        osszes_ertek = df[elemek].to_numpy().flatten()
        osszes_ertek = osszes_ertek[~np.isnan(osszes_ertek)]

        if len(osszes_ertek) == 0:
            raise ValueError("Nincs ábrázolható pozitív adat a táblázatban.")

        adat_min = np.min(osszes_ertek)
        adat_max = np.max(osszes_ertek)

        y_min = adat_min / 10
        y_max = adat_max * 10

        x = np.arange(len(elemek))

        for _, sor in df.iterrows():
            mintaszam = sor[mintaszam_oszlop]

            if pd.isna(mintaszam):
                felirat = ""
            else:
                felirat = str(mintaszam)

            y = sor[elemek].values.astype(float)

            self.ax.plot(
                x,
                y,
                marker="o",
                linewidth=1.5,
                markersize=4,
                label=felirat
            )

        self.ax.set_yscale("log")
        self.ax.set_ylim(y_min, y_max)

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(
            elemek,
            rotation=0,
            ha="center",
            fontstyle="normal"
        )

        self.ax.set_xlabel("Elemek [mg/kg]")
        self.ax.set_ylabel("Koncentráció [mg/kg]")
        self.ax.set_title("Elemkoncentrációk mintánként")

        self.ax.grid(True, which="both", linestyle="--", linewidth=0.5)

        self.ax.legend(
            title=mintaszam_oszlop,
            bbox_to_anchor=(1.02, 1),
            loc="upper left",
            fontsize=8
        )

        self.figure.subplots_adjust(
            left=0.07,
            right=0.78,
            bottom=0.12,
            top=0.92
        )

        self.canvas.draw_idle()

        self.abra_automatikus_mentese(fajlnev)

    def abra_automatikus_mentese(self, fajlnev):
        alapnev = os.path.splitext(os.path.basename(fajlnev))[0]
        mappa = os.path.dirname(fajlnev)

        kimeneti_kep = os.path.join(mappa, f"{alapnev}_diagram.png")

        self.figure.savefig(
            kimeneti_kep,
            dpi=300,
            bbox_inches="tight"
        )

        print(f"Ábra elmentve: {kimeneti_kep}")

    def abra_mentese_kezzel(self):
        if self.aktualis_fajl is None:
            messagebox.showwarning(
                "Nincs ábra",
                "Előbb válassz ki egy Excel fájlt.",
                parent=self.root
            )
            return

        alapnev = os.path.splitext(os.path.basename(self.aktualis_fajl))[0]

        kimeneti_fajl = filedialog.asksaveasfilename(
            parent=self.root,
            title="Ábra mentése",
            defaultextension=".png",
            initialfile=f"{alapnev}_diagram.png",
            filetypes=[
                ("PNG kép", "*.png"),
                ("PDF fájl", "*.pdf"),
                ("SVG fájl", "*.svg"),
                ("Minden fájl", "*.*")
            ]
        )

        if not kimeneti_fajl:
            return

        self.figure.savefig(
            kimeneti_fajl,
            dpi=300,
            bbox_inches="tight"
        )

        print(f"Ábra elmentve: {kimeneti_fajl}")

    def futtatas(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ElemDiagramApp()
    app.futtatas()
