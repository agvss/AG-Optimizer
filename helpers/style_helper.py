# AG_Optimizer/helpers/style_helper.py
# -*- coding: utf-8 -*-
# © 2025 Agustín Bahamondes. Todos los derechos reservados.

def get_app_stylesheet(theme='dark'):
    
    palettes = {
        "dark": {
            "bg": "#121212", "sidebar": "#1E1E1E", "card": "#1E1E1E",
            "border": "#2E2E2E", "text": "#EAEAEA", "text_alt": "#8A8A8A",
            "accent": "#7F5AF0", "accent_text": "#FFFFFF",
            "active_selection": "rgba(127, 90, 240, 0.15)", "active_border": "#7F5AF0"
        },
        "light": {
            "bg": "#F6F6F6", "sidebar": "#FFFFFF", "card": "#FFFFFF",
            "border": "#EBEBEB", "text": "#1A1A1A", "text_alt": "#8A8A8A",
            "accent": "#6E44FF", "accent_text": "#FFFFFF",
            "active_selection": "rgba(110, 68, 255, 0.1)", "active_border": "#6E44FF"
        }
    }
    
    colors = palettes.get(theme, palettes['dark'])

    return f"""
        QMainWindow, QDialog {{ background-color: {colors['bg']}; }}
        QWidget {{ font-family: 'Inter'; color: {colors['text']}; font-size: 14px; }}
        
        /* --- BARRA LATERAL --- */
        QFrame#sidebar {{ background-color: {colors['sidebar']}; border-right: 1px solid {colors['border']}; }}
        QLabel#sidebar_title {{ font-size: 16px; font-weight: bold; padding: 15px 20px; }}
        
        /* --- HEADER --- */
        QFrame#header {{ border-bottom: 1px solid {colors['border']}; }}
        QLabel#pageTitle {{ font-size: 22px; font-weight: bold; }}
        #profileButton {{ border: none; border-radius: 18px; }}
        #headerButton {{ background-color: transparent; border: none; }}

        /* --- TARJETAS --- */
        QFrame.card {{
            background-color: {colors['card']};
            border: 1px solid {colors['border']};
            border-radius: 16px;
        }}
        QLabel.cardTitle {{ font-size: 14px; font-weight: bold; color: {colors['text_alt']}; }}

        /* --- WIDGETS PERSONALIZADOS --- */
        #navButton {{ border-radius: 8px; margin: 4px 10px; }}
        #navButton:hover {{ background-color: {colors['active_selection']}; }}
        #navButton[active="true"] {{ background-color: {colors['active_selection']}; border: 1px solid {colors['active_border']}; }}
        
        #mediaPlayer {{ background-color: {colors['card']}; border-top: 1px solid {colors['border']}; }}
        #mediaButton {{ background-color: transparent; border: none; }}
        #mediaSlider::groove:horizontal {{ height: 4px; background-color: {colors['border']}; border-radius: 2px; }}
        #mediaSlider::handle:horizontal {{ background-color: {colors['text']}; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }}
        #mediaSlider::sub-page:horizontal {{ background-color: {colors['accent']}; border-radius: 2px; }}

        /* --- INTERRUPTOR TIPO IOS --- */
        #iosSwitch {{ max-width: 50px; min-height: 28px; }}
        #iosSwitch > QWidget {{ border-radius: 14px; }}
        #iosSwitch > QWidget > QLabel {{ background-color: #5A5A5A; border-radius: 12px; }}
        #iosSwitch[checked="true"] > QWidget > QLabel {{ background-color: {colors['accent']}; }}
    """