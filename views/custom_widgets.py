# AG_Optimizer/views/custom_widgets.py
# -*- coding: utf-8 -*-
# © 2025 Agustín Bahamondes. Todos los derechos reservados.

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QPushButton
from PySide6.QtCore import Qt, Signal, QSize, QRectF, QPointF, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont, QIcon, QPainter, QPen, QColor, QConicalGradient
from PySide6.QtSvgWidgets import QSvgWidget

class NavButton(QWidget):
    # (El código de esta clase no cambia)
    clicked = Signal()
    def __init__(self, icon_path, text, is_checkable=True):
        super().__init__(); self.setObjectName("navButton"); self.setMinimumHeight(44); self.setCursor(Qt.PointingHandCursor)
        self._is_checkable = is_checkable; self._is_checked = False; layout = QHBoxLayout(self); layout.setContentsMargins(15, 0, 15, 0); layout.setSpacing(15)
        self.icon_widget = QSvgWidget(icon_path); self.icon_widget.setFixedSize(20, 20); self.text_label = QLabel(text); self.text_label.setFont(QFont("Inter", 10, QFont.Medium))
        layout.addWidget(self.icon_widget); layout.addWidget(self.text_label); layout.addStretch()
    def setChecked(self, checked):
        if self._is_checkable and self._is_checked != checked: self._is_checked = checked; self.update_style()
    def mousePressEvent(self, event): self.clicked.emit(); super().mousePressEvent(event)
    def update_style(self):
        if self._is_checked: self.setProperty("active", True); self.text_label.setFont(QFont("Inter", 10, QFont.Bold))
        else: self.setProperty("active", False); self.text_label.setFont(QFont("Inter", 10, QFont.Medium))
        self.style().unpolish(self); self.style().polish(self)

class IOSSwitch(QWidget):
    # (El código de esta clase no cambia)
    toggled = Signal(bool)
    def __init__(self, parent=None):
        super().__init__(parent); self.setObjectName("iosSwitch"); self.setCursor(Qt.PointingHandCursor); self._checked = False
        self.bg_widget = QWidget(self); self.bg_layout = QHBoxLayout(self.bg_widget); self.bg_layout.setContentsMargins(2,2,2,2)
        self.bg_label = QLabel(); self.bg_layout.addWidget(self.bg_label); self.handle = QLabel(self.bg_widget); self.handle.setFixedSize(24, 24); self.handle.setStyleSheet("background-color: white; border-radius: 12px;")
        self.anim = QPropertyAnimation(self.handle, b"pos", self); self.anim.setEasingCurve(QEasingCurve.InOutCubic); self.anim.setDuration(200)
    def setChecked(self, checked):
        self._checked = checked; self.setProperty("checked", checked); self.style().unpolish(self); self.style().polish(self)
        if checked: self.anim.setEndValue(QPoint(self.width() - self.handle.width() - 2, 2))
        else: self.anim.setEndValue(QPoint(2, 2))
        self.anim.start()
    def mousePressEvent(self, event): self.setChecked(not self._checked); self.toggled.emit(self._checked)

class MediaPlayerWidget(QWidget):
    # (El código de esta clase no cambia)
    play_pause_clicked = Signal(); next_clicked = Signal(); prev_clicked = Signal(); volume_changed = Signal(int)
    def __init__(self, parent=None):
        super().__init__(parent); self.setObjectName("mediaPlayer"); self.setFixedHeight(80); layout = QHBoxLayout(self); layout.setContentsMargins(20, 10, 20, 10); layout.setSpacing(15)
        self.prev_btn = QPushButton(icon=QIcon("resources/icons/skip-back.svg")); self.prev_btn.setObjectName("mediaButton"); self.play_btn = QPushButton(icon=QIcon("resources/icons/play-circle.svg")); self.play_btn.setObjectName("mediaButton"); self.play_btn.setIconSize(QSize(32,32)); self.next_btn = QPushButton(icon=QIcon("resources/icons/skip-forward.svg")); self.next_btn.setObjectName("mediaButton")
        track_info_layout = QVBoxLayout(); track_info_layout.setSpacing(0); self.track_title = QLabel("Reproductor Inactivo"); self.track_title.setFont(QFont("Inter", 10, QFont.Bold)); self.track_artist = QLabel("Abre Spotify o un reproductor"); self.track_artist.setStyleSheet("color: #8A8A8A;"); track_info_layout.addWidget(self.track_title); track_info_layout.addWidget(self.track_artist)
        slider_layout = QHBoxLayout(); time_start = QLabel("0:00"); self.slider = QSlider(Qt.Horizontal); self.slider.setObjectName("mediaSlider"); self.slider.setEnabled(False); time_end = QLabel(""); slider_layout.addWidget(time_start); slider_layout.addWidget(self.slider, 1); slider_layout.addWidget(time_end)
        volume_icon = QSvgWidget("resources/icons/volume-2.svg"); volume_icon.setFixedSize(20,20); self.volume_slider = QSlider(Qt.Horizontal); self.volume_slider.setObjectName("mediaSlider"); self.volume_slider.setMaximumWidth(100)
        layout.addWidget(self.prev_btn); layout.addWidget(self.play_btn); layout.addWidget(self.next_btn); layout.addSpacing(10); layout.addLayout(track_info_layout); layout.addLayout(slider_layout, 1); layout.addSpacing(20); layout.addWidget(volume_icon); layout.addWidget(self.volume_slider)
        self.play_btn.clicked.connect(self.play_pause_clicked.emit); self.next_btn.clicked.connect(self.next_clicked.emit); self.prev_btn.clicked.connect(self.prev_clicked.emit); self.volume_slider.valueChanged.connect(self.volume_changed.emit)
    def update_track_info(self, media_info):
        if not media_info or not media_info.get("title"): self.track_title.setText("Reproductor Inactivo"); self.track_artist.setText("Abre Spotify o un reproductor"); self.play_btn.setIcon(QIcon("resources/icons/play-circle.svg")); return
        self.track_title.setText(media_info.get("title", "Desconocido")); self.track_artist.setText(media_info.get("artist", "Desconocido"))
        if media_info.get("is_playing"): self.play_btn.setIcon(QIcon("resources/icons/pause-circle.svg"))
        else: self.play_btn.setIcon(QIcon("resources/icons/play-circle.svg"))
    def set_volume(self, value): self.volume_slider.setValue(value)

class CircularProgressBar(QWidget):
    def __init__(self, title, color1, color2):
        super().__init__(); self.value = 0; self.title = title; self.color1 = QColor(color1); self.color2 = QColor(color2); self.setMinimumSize(180, 180)
    def setValue(self, value): self.value = value; self.update()
    def paintEvent(self, event):
        w, h = self.width(), self.height(); side = min(w, h); painter = QPainter(self); painter.setRenderHint(QPainter.Antialiasing)
        gradient = QConicalGradient(QPointF(side/2, side/2), -90); gradient.setColorAt(0, self.color1); gradient.setColorAt(1, self.color2)
        
        # CORRECCIÓN: Se crea el QPen con el estilo correcto para evitar el TypeError
        bg_pen = QPen(QColor("#2A2A2A"), 14, Qt.SolidLine, Qt.FlatCap)
        painter.setPen(bg_pen); painter.drawArc(QRectF(12, 12, side - 24, side - 24), 0, 360 * 16)
        
        fg_pen = QPen(gradient, 14, Qt.SolidLine, Qt.RoundCap); painter.setPen(fg_pen)
        angle = self.value * 3.6; painter.drawArc(QRectF(12, 12, side - 24, side - 24), 90 * 16, -angle * 16)
        
        painter.setPen(QColor("#E0E0E0")); painter.setFont(QFont("Inter", 26, QFont.Bold)); painter.drawText(QRectF(0,0,side,side), Qt.AlignCenter, f"{int(self.value)}%")
        painter.setPen(QColor("#8E8E8E")); painter.setFont(QFont("Inter", 11, QFont.Medium)); painter.drawText(QRectF(0, 35, side, side), Qt.AlignCenter, self.title)