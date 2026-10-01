from __future__ import annotations

import os
import platform
import shutil
from dataclasses import dataclass

import psutil


@dataclass(frozen=True)
class SystemInfo:
    operating_system: str
    kernel: str
    processor: str
    memory: str
    disk: str
    uptime: str


def _bytes(value: int) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            return f"{amount:.1f} {unit}"
        amount /= 1024
    return f"{amount:.1f} TB"


def _uptime(seconds: float) -> str:
    days, remainder = divmod(int(seconds), 86400)
    hours, minutes = divmod(remainder, 3600)
    minutes //= 60
    if days:
        return f"{days} gün, {hours} saat"
    return f"{hours} saat, {minutes} dakika"


def collect_system_info() -> SystemInfo:
    disk = shutil.disk_usage(os.path.expanduser("~"))
    memory = psutil.virtual_memory()
    return SystemInfo(
        operating_system=f"{platform.system()} {platform.release()}",
        kernel=platform.version(),
        processor=platform.processor() or platform.machine(),
        memory=f"{_bytes(memory.used)} / {_bytes(memory.total)} (%{memory.percent:.0f})",
        disk=f"{_bytes(disk.used)} / {_bytes(disk.total)} (%{disk.used / disk.total * 100:.0f})",
        uptime=_uptime(psutil.boot_time() and __import__("time").time() - psutil.boot_time()),
    )
