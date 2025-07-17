# AG_Optimizer/views/main_window.py
# -*- coding: utf-8 -*-
# © 2025 Agustín Bahamondes. Todos los derechos reservados.

import os
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QStackedWidget, QPushButton
from PySide6.QtGui import QIcon, QFont, QPixmap
from helpers.style_helper import get_app_stylesheet
from helpers.config_helper import load_config, save_config
from views.page_widgets import DashboardPage, OptimizationPage, SettingsPage, NotesPage, CalendarPage
from views.custom_widgets import NavButton, MediaPlayerWidget
from services.media_service import MediaService
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CoInitialize, CoUninitialize, cast, POINTER

class AGOptimizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.setWindowTitle("AG, Optimizer"); self.setMinimumSize(QSize(1280, 800))
        # ... (código del constructor sin cambios) ...
        
        # --- LÓGICA DE AUDIO Y MULTIMEDIA ---
        self.init_audio_interface()
        self.media_service = MediaService()
        self.media_service.media_changed.connect(self.update_media_info)
        self.media_service.start()

    def init_ui(self):
        # ... (código de init_ui sin cambios, pero ahora las páginas son funcionales) ...
        # CONEXIÓN DE PÁGINAS (con las nuevas clases)
        self.pages.addWidget(DashboardPage())
        self.pages.addWidget(OptimizationPage())
        self.pages.addWidget(NotesPage())
        self.pages.addWidget(CalendarPage())
        settings_page = SettingsPage()
        settings_page.theme_changed.connect(self.toggle_theme)
        self.pages.addWidget(settings_page)
        
        self.apply_theme()
        self.switch_page("dashboard")

        # Conectar señales del reproductor
        self.media_player.play_pause_clicked.connect(MediaService.send_play_pause)
        self.media_player.next_clicked.connect(MediaService.send_next)
        self.media_player.prev_clicked.connect(MediaService.send_prev)
        self.media_player.volume_changed.connect(self.set_volume)

    def init_audio_interface(self):
        self.audio_interface = None
        try:
            CoInitialize()
            speakers = AudioUtilities.GetSpeakers()
            interface = speakers.Activate(IAudioEndpointVolume._iid_, 7, None)
            self.audio_interface = cast(interface, POINTER(IAudioEndpointVolume))
            volume = int(self.audio_interface.GetMasterVolumeLevelScalar() * 100)
            self.media_player.set_volume(volume)
        except Exception:
            print("No se pudo inicializar la interfaz de audio.")

    def set_volume(self, value):
        if self.audio_interface:
            self.audio_interface.SetMasterVolumeLevelScalar(value / 100.0, None)

    def update_media_info(self, media_info):
        self.media_player.update_track_info(media_info)

    def toggle_theme(self, theme):
        self.config['theme'] = theme
        save_config(self.config)
        self.apply_theme()

    def closeEvent(self, event):
        self.media_service.stop()
        self.media_service.wait()
        if self.audio_interface:
            CoUninitialize()
        super().closeEvent(event)
    
    # ... (el resto de las funciones como switch_page y apply_theme no cambian) ...