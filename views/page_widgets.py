# AG_Optimizer/views/page_widgets.py
# -*- coding: utf-8 -*-
# © 2025 Agustín Bahamondes. Todos los derechos reservados.

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QGridLayout, QTextEdit, QCalendarWidget
from PySide6.QtCore import Qt, QTimer, QThreadPool, Signal
from PySide6.QtGui import QFont

# --- IMPORTACIONES DE SERVICIOS Y WIDGETS ---
from services.system_service import SystemService
from services.optimization_service import TempCleaner, DNSFlush
from .custom_widgets import CircularProgressBar, IOSSwitch
from helpers.config_helper import save_config, load_config

class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.system_service = SystemService()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 20, 30, 30)
        main_layout.setSpacing(25)
        main_layout.addWidget(QLabel("Dashboard", objectName="pageTitle"))

        grid_layout = QGridLayout()
        grid_layout.setSpacing(25)

        self.cpu_progress = CircularProgressBar("Uso de CPU", "#7F5AF0", "#9D82F2")
        self.ram_progress = CircularProgressBar("Uso de RAM", "#2CB67D", "#4AE3A5")
        
        cpu_card = QFrame(objectName="card")
        cpu_layout = QVBoxLayout(cpu_card)
        cpu_layout.addWidget(self.cpu_progress)
        
        ram_card = QFrame(objectName="card")
        ram_layout = QVBoxLayout(ram_card)
        ram_layout.addWidget(self.ram_progress)

        info_card = QFrame(objectName="card")
        info_layout = QVBoxLayout(info_card)
        info_layout.addWidget(QLabel("Componentes", objectName="cardTitle"))
        info_grid = QGridLayout()
        info_grid.setContentsMargins(15, 10, 15, 15)
        self.cpu_label = QLabel("...")
        self.gpu_label = QLabel("...")
        self.ram_label = QLabel("...")
        info_grid.addWidget(QLabel("<b>CPU</b>"), 0, 0)
        info_grid.addWidget(self.cpu_label, 0, 1)
        info_grid.addWidget(QLabel("<b>GPU</b>"), 1, 0)
        info_grid.addWidget(self.gpu_label, 1, 1)
        info_grid.addWidget(QLabel("<b>RAM</b>"), 2, 0)
        info_grid.addWidget(self.ram_label, 2, 1)
        info_layout.addLayout(info_grid)
        info_layout.addStretch()

        processes_card = QFrame(objectName="card")
        proc_layout = QVBoxLayout(processes_card)
        proc_layout.setContentsMargins(0, 0, 0, 10)
        proc_layout.addWidget(QLabel("Procesos con más RAM", objectName="cardTitle"))
        self.proc_grid = QGridLayout()
        self.proc_grid.setContentsMargins(15, 5, 15, 10)
        proc_layout.addLayout(self.proc_grid)
        proc_layout.addStretch()

        grid_layout.addWidget(cpu_card, 0, 0)
        grid_layout.addWidget(ram_card, 0, 1)
        grid_layout.addWidget(info_card, 1, 0)
        grid_layout.addWidget(processes_card, 1, 1)
        main_layout.addLayout(grid_layout, 1)

        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.update_dynamic_data)
        self.monitor_timer.start(2000)
        self.load_static_data()
        self.update_dynamic_data()
        
    def load_static_data(self):
        info = self.system_service.get_hardware_info()
        self.cpu_label.setText(info['cpu'])
        self.gpu_label.setText(info['gpu'])
        self.ram_label.setText(info['ram'])

    def update_dynamic_data(self):
        self.cpu_progress.setValue(self.system_service.get_cpu_percent())
        self.ram_progress.setValue(self.system_service.get_ram_percent())
        
        while (item := self.proc_grid.takeAt(0)) is not None:
            if item.widget():
                item.widget().deleteLater()
        
        top_processes = self.system_service.get_top_processes_by_ram(5)
        for i, (name, data) in enumerate(top_processes):
            mem_mb = data['rss'] / (1024 * 1024)
            self.proc_grid.addWidget(QLabel(name[:20]), i, 0)
            self.proc_grid.addWidget(QLabel(f"{mem_mb:.1f} MB"), i, 1, Qt.AlignRight)


class OptimizationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread_pool = QThreadPool()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 20, 30, 30)
        main_layout.setSpacing(20)
        main_layout.addWidget(QLabel("Optimización", objectName="pageTitle"))
        
        self.status_label = QLabel("Selecciona una tarea de optimización para comenzar.")
        main_layout.addWidget(self.status_label)
        main_layout.addSpacing(10)

        clean_temp_btn = QPushButton("Limpiar Archivos Temporales")
        clean_temp_btn.setObjectName("primary")
        clean_temp_btn.clicked.connect(self.clean_temp)
        
        flush_dns_btn = QPushButton("Limpiar Caché de DNS")
        flush_dns_btn.setObjectName("primary")
        flush_dns_btn.clicked.connect(self.flush_dns)

        main_layout.addWidget(clean_temp_btn)
        main_layout.addWidget(flush_dns_btn)
        main_layout.addStretch()

    def task_finished(self, message):
        self.status_label.setText(f"✅ {message}")
    
    def task_error(self, message):
        self.status_label.setText(f"❌ {message}")

    def clean_temp(self):
        self.status_label.setText("🧹 Limpiando archivos temporales...")
        worker = TempCleaner()
        worker.signals.finished.connect(self.task_finished)
        worker.signals.error.connect(self.task_error)
        self.thread_pool.start(worker)

    def flush_dns(self):
        self.status_label.setText("🌐 Limpiando caché de DNS...")
        worker = DNSFlush()
        worker.signals.finished.connect(self.task_finished)
        worker.signals.error.connect(self.task_error)
        self.thread_pool.start(worker)


class NotesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.addWidget(QLabel("Notas Rápidas", objectName="pageTitle"))
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Escribe tus notas aquí... Se guardarán automáticamente.")
        self.text_edit.setStyleSheet("background-color: #1E1E1E; border: 1px solid #2E2E2E; border-radius: 12px; padding: 15px;")
        self.text_edit.setText(self.config.get("user_notes", ""))
        self.text_edit.textChanged.connect(self.save_notes)
        layout.addWidget(self.text_edit)

    def save_notes(self):
        self.config["user_notes"] = self.text_edit.toPlainText()
        save_config(self.config)


class CalendarPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.addWidget(QLabel("Calendario", objectName="pageTitle"))
        calendar = QCalendarWidget()
        calendar.setStyleSheet("QCalendarWidget QToolButton { color: white; } QCalendarWidget QAbstractItemView:enabled { color: white; }")
        layout.addWidget(calendar)


class SettingsPage(QWidget):
    theme_changed = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.addWidget(QLabel("Ajustes", objectName="pageTitle"))
        
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Modo Oscuro / Claro"))
        theme_layout.addStretch()
        self.theme_switch = IOSSwitch()
        self.theme_switch.setChecked(self.config.get("theme", "dark") == "dark")
        self.theme_switch.toggled.connect(self.toggle_theme)
        theme_layout.addWidget(self.theme_switch)

        layout.addLayout(theme_layout)
        layout.addStretch()

    def toggle_theme(self, is_dark):
        theme = "dark" if is_dark else "light"
        self.theme_changed.emit(theme)