# AG_Optimizer/views/onboarding_view.py
# -*- coding: utf-8 -*-
# © 2025 Agustín Bahamondes. Todos los derechos reservados.

""" Ventana de bienvenida para la configuración inicial. """

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
import os
from helpers.config_helper import save_config, load_config
from helpers.style_helper import get_app_stylesheet

class OnboardingWindow(QDialog):
    onboarding_finished = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenido a AG, Optimizer")
        self.setMinimumSize(500, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        if os.path.exists(os.path.join("resources", "logo.png")):
            self.setWindowIcon(QIcon(os.path.join("resources", "logo.png")))

        self.setStyleSheet(get_app_stylesheet('light')) # Onboarding siempre en tema claro

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignCenter)

        logo_label = QLabel()
        pixmap = QIcon(os.path.join("resources", "logo.png")).pixmap(64, 64)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        
        title = QLabel("Bienvenido a AG, Optimizer")
        title.setObjectName("welcomeTitle")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Tu asistente personal para un PC más rápido y organizado.")
        subtitle.setObjectName("welcomeSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Por favor, ingresa tu nombre")
        
        continue_btn = QPushButton("Comenzar a Optimizar")
        continue_btn.setObjectName("primary")
        continue_btn.clicked.connect(self.finish_onboarding)
        
        main_layout.addWidget(logo_label)
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(QLabel("¿Cómo deberíamos llamarte?"))
        main_layout.addWidget(self.name_input)
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        main_layout.addWidget(continue_btn, 0, Qt.AlignRight)

    def finish_onboarding(self):
        username = self.name_input.text().strip()
        if not username:
            username = "Usuario" # Nombre por defecto
        
        config = load_config()
        config['username'] = username
        config['onboarding_complete'] = True
        config['theme'] = 'light' # Tema inicial
        save_config(config)
        
        self.onboarding_finished.emit()
        self.accept()