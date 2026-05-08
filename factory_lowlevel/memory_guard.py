"""CB-021 memory-safety guardrails for the Factory daemon.

The 2026-05-08 incident (factory-daemon-incident-report-2026-05-08.md)
documented the daemon eating 40-50 GB of RSS in one long-lived Python
process and white-screening the desktop. The architectural fixes
(sharded persistence, per-source child processes, SQLite migration)
are deferred to a separate ticket; this module ships the
*guardrails* so the same pathological case can't reach system-killing
levels again:

* ``check_memory_budget()`` — query process RSS + system free RAM. If
  RSS exceeds ``MAX_RSS_GB`` (default 24) or system free RAM falls
  below ``MIN_FREE_GB`` (default 8), the caller aborts the cycle
  with a structured diagnostic.
* ``read_stop_flag()`` — file-based safe-stop. The operator drops
  ``control_room/cache/factory_daemon_stop.flag`` and the daemon
  picks it up between bundles + records, exits cleanly.
* ``DEFAULT_MAX_RSS_GB`` / ``DEFAULT_MIN_FREE_GB`` — conservative
  defaults that leave headroom for desktop apps. Override per-launch
  via env vars for testing.

Cross-platform memory query strategy:

1. ``psutil`` if importable (preferred — accurate, simple)
2. Windows ``ctypes`` -> ``psapi.GetProcessMemoryInfo`` +
   ``GlobalMemoryStatusEx`` (no extra deps)
3. Linux ``/proc/self/status`` + ``/proc/meminfo``
4. Last resort: return ``None`` and skip the guard (the daemon
   logs a warning rather than failing closed, since the guard
   itself is best-effort safety, not a correctness invariant).

D9 binding: when the guard fires, the daemon writes a structured
``memory_budget_exceeded`` audit item before exiting so the operator
sees the failure honestly rather than as a silent process death.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


DEFAULT_MAX_RSS_GB = float(os.environ.get("FACTORY_DAEMON_MAX_RSS_GB", "24"))
DEFAULT_MIN_FREE_GB = float(os.environ.get("FACTORY_DAEMON_MIN_FREE_GB", "8"))
DEFAULT_STOP_FLAG_PATH = Path("control_room/cache/factory_daemon_stop.flag")


@dataclass(frozen=True)
class MemorySnapshot:
    """Process RSS + system free RAM in GB. ``None`` for unmeasured."""
    rss_gb: Optional[float]
    free_gb: Optional[float]
    source: str  # "psutil", "windows_ctypes", "linux_proc", "unmeasured"

    def is_measured(self) -> bool:
        return self.rss_gb is not None and self.free_gb is not None


def measure_memory() -> MemorySnapshot:
    """Best-effort cross-platform memory snapshot.

    Returns ``MemorySnapshot(None, None, "unmeasured")`` if no backend
    is available. The caller treats unmeasured as "guard inactive"
    rather than "fail closed" — the guard is safety, not correctness.
    """
    # Try psutil first
    try:
        import psutil  # type: ignore[import-not-found]
        proc = psutil.Process(os.getpid())
        rss_gb = proc.memory_info().rss / (1024 ** 3)
        free_gb = psutil.virtual_memory().available / (1024 ** 3)
        return MemorySnapshot(rss_gb, free_gb, "psutil")
    except ImportError:
        pass
    except Exception:
        pass

    # Try Windows ctypes
    if sys.platform == "win32":
        try:
            return _measure_windows_ctypes()
        except Exception:
            pass

    # Try Linux /proc
    if sys.platform == "linux":
        try:
            return _measure_linux_proc()
        except Exception:
            pass

    return MemorySnapshot(None, None, "unmeasured")


def _measure_windows_ctypes() -> MemorySnapshot:
    """Windows-native RSS + free-RAM via psapi + kernel32."""
    import ctypes
    from ctypes import wintypes

    # PROCESS_MEMORY_COUNTERS struct
    class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD),
            ("PageFaultCount", wintypes.DWORD),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    pmc = PROCESS_MEMORY_COUNTERS()
    pmc.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    psapi.GetProcessMemoryInfo.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(PROCESS_MEMORY_COUNTERS),
        wintypes.DWORD,
    ]
    psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
    handle = kernel32.GetCurrentProcess()
    if not psapi.GetProcessMemoryInfo(handle, ctypes.byref(pmc), pmc.cb):
        err = ctypes.get_last_error()
        raise OSError(f"GetProcessMemoryInfo failed (WinError {err})")
    rss_gb = pmc.WorkingSetSize / (1024 ** 3)

    # GlobalMemoryStatusEx for free RAM
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", wintypes.DWORD),
            ("dwMemoryLoad", wintypes.DWORD),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    msx = MEMORYSTATUSEX()
    msx.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    kernel32.GlobalMemoryStatusEx.argtypes = [ctypes.POINTER(MEMORYSTATUSEX)]
    kernel32.GlobalMemoryStatusEx.restype = wintypes.BOOL
    if not kernel32.GlobalMemoryStatusEx(ctypes.byref(msx)):
        err = ctypes.get_last_error()
        raise OSError(f"GlobalMemoryStatusEx failed (WinError {err})")
    free_gb = msx.ullAvailPhys / (1024 ** 3)

    return MemorySnapshot(rss_gb, free_gb, "windows_ctypes")


def _measure_linux_proc() -> MemorySnapshot:
    """Linux /proc/self/status + /proc/meminfo backend."""
    rss_kb: Optional[int] = None
    with open("/proc/self/status", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("VmRSS:"):
                rss_kb = int(line.split()[1])
                break
    free_kb: Optional[int] = None
    with open("/proc/meminfo", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("MemAvailable:"):
                free_kb = int(line.split()[1])
                break
    rss_gb = (rss_kb / (1024 ** 2)) if rss_kb is not None else None
    free_gb = (free_kb / (1024 ** 2)) if free_kb is not None else None
    return MemorySnapshot(rss_gb, free_gb, "linux_proc")


def check_memory_budget(
    *,
    max_rss_gb: float = DEFAULT_MAX_RSS_GB,
    min_free_gb: float = DEFAULT_MIN_FREE_GB,
) -> tuple[bool, MemorySnapshot, str]:
    """Return ``(ok, snapshot, reason)``.

    * ``ok=True`` if memory headroom is acceptable (or unmeasured).
    * ``ok=False`` if RSS > max_rss_gb OR free < min_free_gb.

    Caller logs ``reason`` to the audit queue on ``ok=False`` and
    initiates clean shutdown.
    """
    snap = measure_memory()
    if not snap.is_measured():
        return True, snap, "memory_unmeasured_guard_inactive"
    if snap.rss_gb is not None and snap.rss_gb > max_rss_gb:
        return False, snap, (
            f"memory_budget_exceeded: RSS {snap.rss_gb:.1f} GB > max {max_rss_gb:.1f} GB"
        )
    if snap.free_gb is not None and snap.free_gb < min_free_gb:
        rss_str = f"{snap.rss_gb:.1f}" if snap.rss_gb is not None else "unknown"
        return False, snap, (
            f"memory_budget_exceeded: system free RAM {snap.free_gb:.1f} GB < min {min_free_gb:.1f} GB "
            f"(process RSS {rss_str} GB)"
        )
    return True, snap, "memory_within_budget"


def read_stop_flag(stop_flag_path: Path = DEFAULT_STOP_FLAG_PATH) -> Optional[str]:
    """Return reason string if the file-based stop flag is set, else None.

    Operator usage:
        echo "user requested stop" > control_room/cache/factory_daemon_stop.flag
    Daemon checks this between bundles + records and exits cleanly.

    The daemon DELETES the stop flag after honoring it so the next
    launch starts cleanly. This means: don't leave the flag on disk
    expecting the next launch to also stop.
    """
    if not stop_flag_path.exists():
        return None
    try:
        reason = stop_flag_path.read_text(encoding="utf-8-sig").strip()
        return reason or "operator_stop_flag_set"
    except OSError:
        return "operator_stop_flag_set_unreadable"


def consume_stop_flag(stop_flag_path: Path = DEFAULT_STOP_FLAG_PATH) -> None:
    """Delete the stop flag after honoring it. Idempotent."""
    try:
        if stop_flag_path.exists():
            stop_flag_path.unlink()
    except OSError:
        pass  # leave for next launch to handle
