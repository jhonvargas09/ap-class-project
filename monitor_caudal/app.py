"""Monitor de Flow (Nm3/h) capturado desde CS Service Flow Sensors por OCR,
graficado contra un valor ingresado manualmente, con registro en Excel.

Ejecutar:  python app.py
"""
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from capture import read_number_from_region
from data_store import DataStore
from excel_logger import ExcelLogger
from plotting import PlotWindow
from region_selector import RegionSelector

POLL_INTERVAL_SECONDS = 1.0
EXCEL_PATH = "flow_log.xlsx"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Flow - CS Service Flow Sensors")
        self.root.resizable(False, False)

        self.region = None
        self.data_store = DataStore()
        self.excel_logger = ExcelLogger(EXCEL_PATH)
        self.last_flow = None
        self.polling = False
        self.poll_thread = None
        self.plot_window = None

        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self.root, padding=12)
        frm.grid()

        ttk.Button(frm, text="Seleccionar región del dato Flow", command=self.select_region)\
            .grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Button(frm, text="Probar lectura", command=self.test_read)\
            .grid(row=1, column=0, columnspan=2, sticky="ew", pady=(4, 0))

        self.region_label = ttk.Label(frm, text="Región: no seleccionada")
        self.region_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 0))

        ttk.Separator(frm, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        ttk.Label(frm, text="Valor a ingresar:").grid(row=4, column=0, sticky="w")
        self.setpoint_entry = ttk.Entry(frm, width=15)
        self.setpoint_entry.grid(row=4, column=1, sticky="e")
        self.setpoint_entry.bind("<Return>", lambda e: self.submit_setpoint())

        ttk.Button(frm, text="Enviar valor", command=self.submit_setpoint)\
            .grid(row=5, column=0, columnspan=2, sticky="ew", pady=(4, 0))

        ttk.Separator(frm, orient="horizontal").grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)

        self.status_label = ttk.Label(frm, text="Flow actual: -- Nm3/h   |   Valor ingresado: --")
        self.status_label.grid(row=7, column=0, columnspan=2, sticky="w")

        btns = ttk.Frame(frm)
        btns.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        btns.columnconfigure((0, 1, 2), weight=1)

        self.start_btn = ttk.Button(btns, text="Iniciar", command=self.start)
        self.start_btn.grid(row=0, column=0, sticky="ew", padx=2)

        self.stop_btn = ttk.Button(btns, text="Detener", command=self.stop, state="disabled")
        self.stop_btn.grid(row=0, column=1, sticky="ew", padx=2)

        ttk.Button(btns, text="Abrir gráfica", command=self.open_plot)\
            .grid(row=0, column=2, sticky="ew", padx=2)

        self.excel_label = ttk.Label(frm, text=f"Registrando en: {EXCEL_PATH}", foreground="grey")
        self.excel_label.grid(row=9, column=0, columnspan=2, sticky="w", pady=(10, 0))

    # --- Región y prueba de lectura -------------------------------------------------

    def select_region(self):
        RegionSelector(self.root, self._on_region_selected)

    def _on_region_selected(self, region):
        self.region = region
        self.region_label.config(text=f"Región: {region}")

    def test_read(self):
        if not self.region:
            messagebox.showerror("Falta región", "Primero selecciona la región del dato Flow.")
            return
        value = read_number_from_region(self.region)
        if value is None:
            messagebox.showwarning("Sin lectura", "No se pudo reconocer un número en esa región. "
                                                    "Intenta ajustar la selección para que cubra solo el número.")
        else:
            messagebox.showinfo("Lectura de prueba", f"Valor detectado: {value}")

    # --- Valor ingresado por el usuario ----------------------------------------------

    def submit_setpoint(self):
        raw = self.setpoint_entry.get().strip().replace(",", ".")
        if not raw:
            return
        try:
            value = float(raw)
        except ValueError:
            messagebox.showerror("Valor inválido", "Ingresa un número válido.")
            return
        self.data_store.set_setpoint(value)
        self._update_status()

    # --- Iniciar / detener captura ----------------------------------------------------

    def start(self):
        if not self.region:
            messagebox.showerror("Falta región", "Selecciona primero la región de pantalla del dato Flow.")
            return
        if self.data_store.current_setpoint is None:
            messagebox.showerror("Falta valor", "Ingresa y envía un valor inicial antes de iniciar.")
            return

        self.polling = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.poll_thread.start()

    def stop(self):
        self.polling = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

    def _poll_loop(self):
        while self.polling:
            value = read_number_from_region(self.region)
            if value is not None and value != self.last_flow:
                self.last_flow = value
                now = datetime.now()
                setpoint = self.data_store.current_setpoint
                self.data_store.add_point(now, value)
                self.excel_logger.log(value, setpoint)
                self.root.after(0, self._update_status)
            time.sleep(POLL_INTERVAL_SECONDS)

    def _update_status(self):
        flow_txt = "--" if self.last_flow is None else str(self.last_flow)
        sp = self.data_store.current_setpoint
        sp_txt = "--" if sp is None else str(sp)
        self.status_label.config(text=f"Flow actual: {flow_txt} Nm3/h   |   Valor ingresado: {sp_txt}")

    # --- Gráfica ------------------------------------------------------------------------

    def open_plot(self):
        self.plot_window = PlotWindow(self.root, self.data_store)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
