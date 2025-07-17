# AG_Optimizer/services/system_service.py
# -*- coding: utf-8 -*-
# © 2025 Agustín Bahamondes. Todos los derechos reservados.

"""
Servicio encargado de obtener toda la información del sistema.
Utiliza psutil para datos de rendimiento y WMI para detalles de hardware en Windows.
"""

import psutil
import platform
from collections import defaultdict

class SystemService:
    def __init__(self):
        self.wmi_conn = None
        # Si es Windows, intenta inicializar la conexión WMI
        if platform.system() == "Windows":
            try:
                import wmi
                self.wmi_conn = wmi.WMI()
            except ImportError:
                print("Advertencia: La librería WMI no está instalada. No se mostrará información detallada de CPU/GPU.")
                self.wmi_conn = None
            except Exception as e:
                print(f"Error al inicializar WMI: {e}")
                self.wmi_conn = None

    def get_cpu_percent(self):
        """Obtiene el porcentaje de uso actual de la CPU."""
        return psutil.cpu_percent()

    def get_ram_percent(self):
        """Obtiene el porcentaje de uso de la RAM."""
        return psutil.virtual_memory().percent

    def get_hardware_info(self):
        """Obtiene información estática del hardware (CPU, GPU, RAM)."""
        info = {
            "cpu": "No disponible",
            "gpu": "No disponible",
            "ram": f"{psutil.virtual_memory().total / (1024**3):.2f} GB"
        }
        
        # Usar WMI para info detallada en Windows
        if self.wmi_conn:
            try:
                info["cpu"] = self.wmi_conn.Win32_Processor()[0].Name.strip()
                info["gpu"] = self.wmi_conn.Win32_VideoController()[0].Name.strip()
            except Exception as e:
                print(f"No se pudo obtener la información de hardware vía WMI: {e}")
                # Fallback por si WMI falla
                info["cpu"] = platform.processor()
        else:
            # Fallback para otros SO o si WMI no está disponible
            info["cpu"] = platform.processor()
            
        return info

    def get_top_processes_by_ram(self, count=4):
        """Obtiene una lista de los 'count' procesos que más RAM consumen."""
        process_map = defaultdict(lambda: {"rss": 0})
        
        for p in psutil.process_iter(['name', 'memory_info']):
            try:
                # Agrupamos por nombre de proceso para consolidar (ej: chrome.exe)
                process_map[p.info['name']]['rss'] += p.info['memory_info'].rss
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Ordenamos por memoria (rss) de forma descendente y tomamos el top 'count'
        sorted_processes = sorted(process_map.items(), key=lambda item: item[1]['rss'], reverse=True)
        
        return sorted_processes[:count]