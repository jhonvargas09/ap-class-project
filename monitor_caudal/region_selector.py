"""Overlay de pantalla completa para que el usuario arrastre y seleccione
la región donde el software CS Service Flow Sensors muestra el dato Flow."""
import tkinter as tk


class RegionSelector:
    def __init__(self, master, on_select):
        self.on_select = on_select
        self.start_x = None
        self.start_y = None
        self.rect_id = None

        self.top = tk.Toplevel(master)
        self.top.attributes("-fullscreen", True)
        self.top.attributes("-alpha", 0.3)
        self.top.attributes("-topmost", True)
        self.top.configure(bg="grey11")
        self.top.bind("<Escape>", lambda e: self.top.destroy())

        hint = tk.Label(
            self.top,
            text="Arrastra el mouse sobre el dato Flow y suelta. Esc para cancelar.",
            fg="white",
            bg="grey11",
            font=("Segoe UI", 14),
        )
        hint.pack(pady=20)

        self.canvas = tk.Canvas(self.top, cursor="cross", bg="grey11", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        # Coordenadas absolutas de pantalla: el canvas no empieza en (0,0) del
        # Toplevel (la etiqueta de arriba lo desplaza), así que event.x/event.y
        # (locales al canvas) no sirven para calcular la región de captura.
        self.start_x, self.start_y = event.x_root, event.y_root
        self.rect_id = self.canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline="red", width=2,
        )

    def _on_drag(self, event):
        start_x_local = self.start_x - self.canvas.winfo_rootx()
        start_y_local = self.start_y - self.canvas.winfo_rooty()
        self.canvas.coords(self.rect_id, start_x_local, start_y_local, event.x, event.y)

    def _on_release(self, event):
        x0, y0 = self.start_x, self.start_y
        x1, y1 = event.x_root, event.y_root
        left, right = sorted((x0, x1))
        top, bottom = sorted((y0, y1))
        width, height = right - left, bottom - top
        self.top.destroy()

        if width < 5 or height < 5:
            return

        region = {"left": left, "top": top, "width": width, "height": height}
        self.on_select(region)
