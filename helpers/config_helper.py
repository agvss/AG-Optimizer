# AG_Optimizer/helpers/config_helper.py
# -*- coding: utf-8 -*-
# © 2025 Agustín Bahamondes. Todos los derechos reservados.

""" Módulo para gestionar la configuración de la aplicación. """

import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """ Carga la configuración desde config.json. Si no existe, devuelve un dict vacío. """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_config(config_data):
    """ Guarda el diccionario de configuración en config.json. """
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)
    except IOError as e:
        print(f"Error al guardar la configuración: {e}")