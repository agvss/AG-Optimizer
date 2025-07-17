# AG_Optimizer/main.py
# -*- coding: utf-8 -*-
# © 2025 Agustín Bahamondes. Todos los derechos reservados.

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFontDatabase
from views.splash_view import SplashScreen
from views.main_window import AGOptimizerApp
from views.onboarding_view import OnboardingWindow
from helpers.config_helper import load_config

if __name__ == "__main__":
    # CORRECCIÓN 1: Esta configuración ahora se ejecuta ANTES de crear la aplicación.
    if hasattr(QApplication, 'setHighDpiScaleFactorRoundingPolicy'):
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    
    # --- CARGA DE FUENTES PERSONALIZADAS ---
    font_dir = os.path.join("resources", "fonts")
    regular_font_path = os.path.join(font_dir, "Inter_18pt-Regular.ttf")
    bold_font_path = os.path.join(font_dir, "Inter_18pt-Bold.ttf")
    
    if os.path.exists(regular_font_path) and os.path.exists(bold_font_path):
        QFontDatabase.addApplicationFont(regular_font_path)
        QFontDatabase.addApplicationFont(bold_font_path)
    else:
        print("ADVERTENCIA: No se encontraron los archivos de la fuente 'Inter' en 'resources/fonts/'. Se usará una fuente de sistema.")
    
    config = load_config()
    main_win = None

    def launch_main_app():
        global main_win
        logo_path = os.path.join("resources", "logo.png")
        splash = SplashScreen(logo_path)
        splash.show()
        
        def show_main():
            global main_win
            main_win = AGOptimizerApp()
            main_win.show()
            splash.finish(main_win)
        
        QTimer.singleShot(2000, show_main)

    if config.get('onboarding_complete', False):
        launch_main_app()
    else:
        onboarding_win = OnboardingWindow()
        onboarding_win.onboarding_finished.connect(launch_main_app)
        onboarding_win.exec()

    sys.exit(app.exec())