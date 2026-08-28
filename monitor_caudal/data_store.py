"""Almacén de datos compartido entre el hilo de captura y la ventana de gráfica."""
import threading


class DataStore:
    def __init__(self):
        self._lock = threading.Lock()
        self.times = []
        self.flows = []
        self.setpoints = []
        self.current_setpoint = None

    def add_point(self, timestamp, flow_value):
        with self._lock:
            self.times.append(timestamp)
            self.flows.append(flow_value)
            self.setpoints.append(self.current_setpoint)

    def set_setpoint(self, value):
        with self._lock:
            self.current_setpoint = value

    def snapshot(self):
        with self._lock:
            return list(self.times), list(self.flows), list(self.setpoints)

    def clear(self):
        with self._lock:
            self.times.clear()
            self.flows.clear()
            self.setpoints.clear()
