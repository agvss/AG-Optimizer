# AG_Optimizer/services/media_service.py
# -*- coding: utf-8 -*-
# © 2025 Agustín Bahamondes. Todos los derechos reservados.

import asyncio
from threading import Thread
from PySide6.QtCore import QObject, Signal, QThread

try:
    from pywinrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
    IS_AVAILABLE = True
except ImportError:
    IS_AVAILABLE = False

class MediaService(QThread):
    media_changed = Signal(dict)

    def __init__(self):
        super().__init__()
        self.running = True
        self.loop = None

    async def _get_media_info(self):
        if not IS_AVAILABLE: return None
        try:
            manager = await MediaManager.request_async()
            session = manager.get_current_session()
            if session:
                info = await session.try_get_media_properties_async()
                return {
                    "artist": info.artist, "title": info.title,
                    "is_playing": session.get_playback_info().playback_status == 3
                }
        except Exception: pass
        return None

    async def _main_loop(self):
        last_info = {}
        while self.running:
            current_info = await self._get_media_info()
            if current_info and current_info != last_info:
                self.media_changed.emit(current_info)
                last_info = current_info
            await asyncio.sleep(2)

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._main_loop())

    def stop(self):
        self.running = False

    @staticmethod
    def _run_command_in_thread(command):
        """ Ejecuta un comando async en un hilo separado para no bloquear. """
        async def _send_command_async():
            if not IS_AVAILABLE: return
            try:
                manager = await MediaManager.request_async()
                session = manager.get_current_session()
                if session:
                    if command == "play_pause": await session.try_toggle_play_pause_async()
                    elif command == "next": await session.try_skip_next_async()
                    elif command == "prev": await session.try_skip_previous_async()
            except Exception: pass
        
        Thread(target=lambda: asyncio.run(_send_command_async())).start()

    @classmethod
    def send_play_pause(cls): cls._run_command_in_thread("play_pause")
    @classmethod
    def send_next(cls): cls._run_command_in_thread("next")
    @classmethod
    def send_prev(cls): cls._run_command_in_thread("prev")