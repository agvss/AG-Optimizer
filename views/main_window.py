# AG_Optimizer/views/main_window.py
# -*- coding: utf-8 -*-
# © 2025 Agustín Bahamondes. Todos los derechos reservados.

import os, sys
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QStackedWidget, QPushButton
from PySide6.QtGui import QIcon, QFont, QPixmap
from helpers.style_helper import get_app_stylesheet
from helpers.config_helper import load_config, save_config
from views.page_widgets import DashboardPage, OptimizationPage, SettingsPage, NotesPage, CalendarPage
from views.custom_widgets import NavButton, MediaPlayerWidget
from services.media_service import MediaService

try:
    from comtypes import CoInitialize, CoUninitialize
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    AUDIO_ENABLED = True
except (ImportError, OSError):
    AUDIO_ENABLED = False

class AGOptimizerApp(QMainWindow):
    def __init__(self):
        super().__init__(); self.config = load_config(); self.audio_interface = None
        self.setWindowTitle("AG, Optimizer"); self.setMinimumSize(QSize(1280, 800))
        if os.path.exists(os.path.join("resources", "logo.png")): self.setWindowIcon(QIcon(os.path.join("resources", "logo.png")))
        
        self.init_ui()
        self.apply_theme()
        
        self.init_audio_interface()
        self.media_service = MediaService()
        self.media_service.media_changed.connect(self.update_media_info)
        self.media_service.start()

    def init_ui(self):
        main_widget = QWidget(); self.setCentralWidget(main_widget)
        app_layout = QHBoxLayout(main_widget); app_layout.setContentsMargins(0,0,0,0); app_layout.setSpacing(0)
        sidebar = QFrame(objectName="sidebar"); sidebar.setFixedWidth(260); app_layout.addWidget(sidebar)
        sidebar_layout = QVBoxLayout(sidebar); sidebar_layout.setContentsMargins(0, 20, 0, 20); sidebar_layout.setSpacing(5)
        logo_label = QLabel("AG, Optimizer"); logo_label.setObjectName("sidebar_title"); logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(logo_label); sidebar_layout.addSpacing(20)

        content_container = QVBoxLayout(); content_container.setContentsMargins(0,0,0,0); content_container.setSpacing(0)
        app_layout.addLayout(content_container, 1)

        header = QFrame(objectName="header"); header_layout = QHBoxLayout(header); header_layout.setContentsMargins(30, 10, 30, 10)
        self.page_title = QLabel("Dashboard"); self.page_title.setObjectName("pageTitle")
        
        profile_btn = QPushButton(objectName="headerButton"); profile_layout = QHBoxLayout(profile_btn)
        profile_pic = QLabel(); profile_pic.setFixedSize(36, 36); pixmap = QPixmap(os.path.join("resources", "images", "profile.png")); profile_pic.setPixmap(pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation)); profile_pic.setStyleSheet("border-radius: 18px;")
        user_name_label = QLabel(self.config.get('username', 'Usuario')); user_name_label.setFont(QFont("Inter", 10, QFont.Bold))
        profile_layout.addWidget(profile_pic); profile_layout.addWidget(user_name_label)
        
        settings_btn = QPushButton(icon=QIcon("resources/icons/settings.svg")); settings_btn.setObjectName("headerButton")
        
        header_layout.addWidget(self.page_title); header_layout.addStretch(); header_layout.addWidget(profile_btn); header_layout.addWidget(settings_btn)
        content_container.addWidget(header)
        
        self.pages = QStackedWidget(); content_container.addWidget(self.pages, 1)
        self.media_player = MediaPlayerWidget(); content_container.addWidget(self.media_player)

        self.nav_buttons = {
            "dashboard": NavButton("resources/icons/layout-dashboard.svg", "Dashboard"),
            "optimization": NavButton("resources/icons/shield-check.svg", "Optimización"),
            "notes": NavButton("resources/icons/notebook-pen.svg", "Notas Rápidas"),
            "calendar": NavButton("resources/icons/calendar-days.svg", "Calendario"),
            "settings": NavButton("resources/icons/sliders-horizontal.svg", "Ajustes"),
        }
        for name, button in self.nav_buttons.items():
            button.clicked.connect(lambda name=name: self.switch_page(name))
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()
        help_button = NavButton("resources/icons/message-circle-question.svg", "Ayuda", is_checkable=False)
        sidebar_layout.addWidget(help_button)
        
        # Conexión de páginas funcionales
        self.pages.addWidget(DashboardPage())
        self.pages.addWidget(OptimizationPage())
        self.pages.addWidget(NotesPage())
        self.pages.addWidget(CalendarPage())
        settings_page = SettingsPage(); settings_page.theme_changed.connect(self.toggle_theme); self.pages.addWidget(settings_page)
        
        self.switch_page("dashboard")
        self.media_player.play_pause_clicked.connect(MediaService.send_play_pause); self.media_player.next_clicked.connect(MediaService.send_next)
        self.media_player.prev_clicked.connect(MediaService.send_prev); self.media_player.volume_changed.connect(self.set_volume)

    def init_audio_interface(self):
        if not AUDIO_ENABLED: self.media_player.volume_slider.setEnabled(False); return
        try:
            CoInitialize()
            from comtypes import cast, POINTER
            speakers = AudioUtilities.GetSpeakers(); interface = speakers.Activate(IAudioEndpointVolume._iid_, 7, None)
            self.audio_interface = cast(interface, POINTER(IAudioEndpointVolume))
            volume = int(self.audio_interface.GetMasterVolumeLevelScalar() * 100)
            self.media_player.set_volume(volume)
        except Exception as e: print(f"No se pudo inicializar la interfaz de audio: {e}"); self.media_player.volume_slider.setEnabled(False)

    def set_volume(self, value):
        if self.audio_interface: self.audio_interface.SetMasterVolumeLevelScalar(value / 100.0, None)

    def update_media_info(self, media_info): self.media_player.update_track_info(media_info)

    def toggle_theme(self, theme):
        self.config['theme'] = theme; save_config(self.config); self.apply_theme()

    def apply_theme(self): self.setStyleSheet(get_app_stylesheet(self.config.get('theme', 'dark')))

    def switch_page(self, name):
        self.page_title.setText(name.replace("_", " ").title())
        for btn_name, button in self.nav_buttons.items(): button.setChecked(btn_name == name)
        self.pages.setCurrentIndex(list(self.nav_buttons.keys()).index(name))

    def closeEvent(self, event):
        self.media_service.stop(); self.media_service.wait()
        if AUDIO_ENABLED and self.audio_interface: CoUninitialize()
        super().closeEvent(event)