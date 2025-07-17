# AG_Optimizer/services/optimization_service.py
# -*- coding: utf-8 -*-
# © 2025 Agustín Bahamondes. Todos los derechos reservados.

import os
import shutil
import tempfile
import subprocess
from PySide6.QtCore import QObject, Signal, QRunnable

class WorkerSignals(QObject):
    finished = Signal(str)
    error = Signal(str)

class TempCleaner(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()

    def run(self):
        try:
            temp_dir = tempfile.gettempdir()
            cleaned_count = 0
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    cleaned_count += 1
                except (PermissionError, OSError):
                    continue
            self.signals.finished.emit(f"Limpieza de temporales completada. {cleaned_count} elementos eliminados.")
        except Exception as e:
            self.signals.error.emit(f"Error al limpiar temporales: {e}")

class DNSFlush(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()

    def run(self):
        try:
            if os.name == 'nt':
                subprocess.run(["ipconfig", "/flushdns"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                self.signals.finished.emit("El caché de DNS ha sido limpiado exitosamente.")
            else:
                self.signals.error.emit("Esta función solo está disponible en Windows.")
        except Exception as e:
            self.signals.error.emit(f"Error al limpiar DNS: {e}. Prueba ejecutar como administrador.")