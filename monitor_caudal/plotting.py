"""Ventana separada con la gráfica en vivo: Flow capturado vs valor ingresado."""
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

REFRESH_MS = 1000


class PlotWindow:
    def __init__(self, master, data_store):
        self.data_store = data_store
        self._closed = False

        self.top = tk.Toplevel(master)
        self.top.title("Gráfica: Flow vs valor ingresado")
        self.top.geometry("800x550")
        self.top.protocol("WM_DELETE_WINDOW", self._on_close)

        self.fig = Figure(figsize=(7, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.top)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self._redraw()

    def _on_close(self):
        self._closed = True
        self.top.destroy()

    def _redraw(self):
        if self._closed:
            return

        times, flows, setpoints = self.data_store.snapshot()
        self.ax.clear()
        if times:
            self.ax.plot(times, flows, marker="o", color="#2563eb", label="Flow (Nm3/h)")
            self.ax.step(times, setpoints, where="post", color="#dc2626", label="Valor ingresado")
            self.fig.autofmt_xdate()
        self.ax.set_xlabel("Tiempo")
        self.ax.set_ylabel("Nm3/h")
        self.ax.set_title("Flow capturado vs valor ingresado")
        self.ax.legend(loc="upper left")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()

        self.top.after(REFRESH_MS, self._redraw)
