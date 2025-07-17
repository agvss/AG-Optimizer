# AG_Optimizer/views/splash_view.py
# -*- coding: utf-8 -*-
# © 2025 Agustín Bahamondes. Todos los derechos reservados.

""" Splash Screen animado que se muestra al iniciar la aplicación. """

from PySide6.QtWidgets import QSplashScreen, QVBoxLayout, QLabel, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, Property

class SplashScreen(QSplashScreen):
    def __init__(self, logo_path):
        super().__init__(QPixmap(1, 1))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.container = QFrame(self)
        self.container.setFixedSize(400, 250)
        self.container.setStyleSheet("background-color: #f2f2f7; border-radius: 20px;")
        
        layout = QVBoxLayout(self.container)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.logo_label = QLabel(self.container)
        pixmap = QPixmap(logo_path)
        self.logo_label.setPixmap(pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)

        title_label = QLabel("AG, Optimizer", self.container)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #000; margin-top: 10px;")

        copyright_label = QLabel("© 2025 Agustín Bahamondes. Todos los derechos reservados.", self.container)
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("font-size: 10px; color: #888; margin-top: 5px;")
        
        layout.addWidget(self.logo_label)
        layout.addWidget(title_label)
        layout.addWidget(copyright_label)

        self.resize(self.container.size())
        
        self.setup_animations()

    def _get_geometry(self):
        return self.container.geometry()

    def _set_geometry(self, rect):
        self.container.setGeometry(rect)

    geometry = Property(QRect, _get_geometry, _set_geometry)

    def setup_animations(self):
        """ Configura las animaciones de entrada. """
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity", self)
        self.fade_in_animation.setDuration(1200)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InOutQuad)

        # CORRECCIÓN: Se accede a 'self.geometry' como una propiedad (sin paréntesis)
        center = self.geometry.center()
        self.scale_animation = QPropertyAnimation(self, b"geometry", self)
        self.scale_animation.setDuration(1000)
        start_rect = QRect(center.x(), center.y(), 0, 0)
        
        # Obtenemos el rectángulo final a partir de la propiedad