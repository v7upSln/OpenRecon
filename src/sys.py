import platform
import psutil
import socket
import getpass
import locale
import os
import subprocess
import re

def get_linux_distro():
    try:
        with open("/etc/os-release") as f:
            data = f.read()
        name = re.search(r'^NAME="?(.*?)"?$', data, re.MULTILINE)
        version = re.search(r'^VERSION="?(.*?)"?$', data, re.MULTILINE)
        return (name.group(1) if name else "Linux", version.group(1) if version else "")
    except Exception:
        return ("Linux", "")

def get_motherboard_info():
    if platform.system() == "Windows":
        try:
            import win32com.client
            wmi = win32com.client.Dispatch("WbemScripting.SWbemLocator")
            service = wmi.ConnectServer(".", "root\\cimv2")
            for board in service.ExecQuery("Select * from Win32_BaseBoard"):
                return board.Product
        except Exception:
            return "Unknown"
    elif platform.system() == "Linux":
        try:
            with open("/sys/devices/virtual/dmi/id/board_name") as f:
                return f.read().strip()
        except Exception:
            return "Unknown"
    return "Unknown"

def get_monitor_names_from_registry():
    monitor_names = {}
    if platform.system() == "Windows":
        try:
            import winreg
            reg_path = r"SYSTEM\CurrentControlSet\Enum\DISPLAY"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as display_key:
                for i in range(winreg.QueryInfoKey(display_key)[0]):
                    mfg_key_name = winreg.EnumKey(display_key, i)
                    with winreg.OpenKey(display_key, mfg_key_name) as mfg_key:
                        for j in range(winreg.QueryInfoKey(mfg_key)[0]):
                            model_key_name = winreg.EnumKey(mfg_key, j)
                            with winreg.OpenKey(mfg_key, model_key_name) as model_key:
                                try:
                                    with winreg.OpenKey(model_key, "Device Parameters") as params_key:
                                        edid_raw, _ = winreg.QueryValueEx(params_key, "EDID")
                                        edid = bytearray(edid_raw)
                                        name = None
                                        for k in range(54, 126, 18):
                                            if edid[k:k+3] == b'\x00\x00\xfc':
                                                name = edid[k+5:k+18].decode(errors="ignore").strip()
                                                break
                                        if name:
                                            monitor_names[model_key_name] = name
                                except Exception:
                                    continue
        except Exception:
            pass
    return monitor_names

def get_gpu_info():
    gpus = []
    system = platform.system()
    if system == "Windows":
        try:
            result = subprocess.run(
                ['wmic', 'path', 'win32_VideoController', 'get', 'Name'],
                capture_output=True, text=True, check=True, timeout=5
            )
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:
                name = line.strip()
                if name:
                    gpus.append(name)
        except Exception:
            pass
    elif system == "Linux":
        try:
            result = subprocess.run(
                "lspci | grep VGA", shell=True,
                capture_output=True, text=True, check=True, timeout=5
            )
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line:
                    gpus.append(line)
        except Exception:
            pass
    return gpus

def get_windows_displays():
    displays = []
    try:
        import win32api
        import win32con
        monitor_info = win32api.EnumDisplayMonitors()
        for monitor in monitor_info:
            hMonitor, hdcMonitor, rect = monitor
            info = win32api.GetMonitorInfo(hMonitor)
            device = info.get('Device', 'Unknown')
            devmode = win32api.EnumDisplaySettings(device, win32con.ENUM_CURRENT_SETTINGS)
            resolution = f"{devmode.PelsWidth}x{devmode.PelsHeight} @{devmode.DisplayFrequency}Hz"
            # Try to get friendly name from registry
            monitor_names = get_monitor_names_from_registry()
            friendly_name = monitor_names.get(device.split("\\")[-1], device)
            displays.append({"name": friendly_name, "resolution": resolution})
    except Exception:
        pass
    return displays if displays else [{"name": "No displays detected", "resolution": ""}]

def get_linux_displays():
    displays = []
    try:
        output = subprocess.check_output(["xrandr", "--listmonitors"], text=True)
        lines = output.strip().splitlines()
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 4:
                name = parts[-1]
                resolution = parts[2]
                displays.append({"name": name, "resolution": resolution})
        if not displays:
            output = subprocess.check_output("xrandr | grep '*'", shell=True, text=True)
            for line in output.strip().splitlines():
                res = line.strip().split()[0]
                displays.append({"name": "Unknown", "resolution": res})
    except Exception:
        pass
    return displays if displays else [{"name": "No displays detected", "resolution": ""}]

def get_windows_update_info():
    try:
        ps_script = "(Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion').DisplayVersion"
        result = subprocess.run(['powershell', '-Command', ps_script],
                                capture_output=True, text=True, check=True, timeout=5)
        update_info = result.stdout.strip()
        return f"({update_info})" if update_info else ""
    except Exception:
        return ""

def get_system_info():
    info = {}
    system = platform.system()
    info['os'] = system
    info['user'] = getpass.getuser()
    info['hostname'] = platform.node()
    info['architecture'] = platform.machine()
    info['platform'] = platform.platform()
    info['shell'] = os.environ.get("SHELL", "sh") if system == "Linux" else os.environ.get("COMSPEC", "CMD")

    # Uptime
    try:
        uptime_seconds = psutil.boot_time()
        uptime = int(psutil.time.time() - uptime_seconds)
        info['uptime'] = uptime
    except Exception:
        info['uptime'] = 0

    # Distro and kernel
    if system == "Linux":
        distro, version = get_linux_distro()
        info['distro'] = distro
        info['os_release'] = platform.release()
        info['os_version'] = version
    elif system == "Windows":
        info['distro'] = "Windows"
        info['os_release'] = platform.version()
        info['os_version'] = get_windows_update_info()
    elif system == "Darwin":
        info['distro'] = "macOS"
        info['os_release'] = platform.mac_ver()[0]
        info['os_version'] = ""

    # CPU
    info['processor'] = platform.processor() or os.environ.get("PROCESSOR_IDENTIFIER", "Unknown")

    # GPU
    info['gpu'] = get_gpu_info()

    # Memory
    mem = psutil.virtual_memory()
    info['memory'] = {
        "used": mem.used,
        "total": mem.total,
        "percent": mem.percent
    }

    # Swap
    swap = psutil.swap_memory()
    info['swap'] = {
        "used": swap.used,
        "total": swap.total,
        "percent": swap.percent
    }

    # Disks (Windows only)
    disks = []
    if system == "Windows":
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disks.append({
                    "device": part.device,
                    "mount": part.mountpoint,
                    "used": usage.used,
                    "total": usage.total,
                    "percent": usage.percent,
                    "fstype": part.fstype
                })
            except Exception:
                continue
    info['disks'] = disks

    # Display
    if system == "Windows":
        info['display'] = {"displays": get_windows_displays()}
    elif system == "Linux":
        info['display'] = {"displays": get_linux_displays()}
    else:
        info['display'] = {"displays": [{"name": "Unknown", "resolution": ""}]}

    # Network IPs
    ip_addresses = {}
    for iface, addrs in psutil.net_if_addrs().items():
        ip_addresses[iface] = [addr.address for addr in addrs if addr.family == socket.AF_INET]
    info['ip_addresses'] = ip_addresses
    
    # Locale
    info['locale'] = locale.getdefaultlocale()[0] or "Unknown"
    
    if system =="Linux":
        #DE
        desktop_env = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION") or "Unknown"
        info['desktop_env'] = desktop_env
        
        #WM
        wm = os.environ.get("XDG_SESSION_TYPE", "")
        if not wm or wm == "x11":
            try:
                #try to get WM from an active process
                import subprocess
                result = subprocess.run("wmctrl -m", shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    for line in result.stdout.splitlines():
                        if line.lower().startswith("name:"):
                            wm = line.split(":", 1)[1].strip()
                            break
            except Exception:
                pass
        if not wm:
            wm - "Unknown"
        info['window_manager'] = wm
    return info

    return info

def format_bytes(size):
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PiB"

def format_uptime(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours} hours, {minutes} mins"

def get_os_banner_name(info):
    os_name = info.get("os", "").lower()
    distro = info.get("distro", "").lower()
    # List of supported banner names
    known_banners = {
        "ubuntu", "arch", "debian", "fedora", "mint", "manjaro", "deepin", "raspberry", "redhat", "redhat2",
        "steamos", "steamos2", "vanilla", "eurolinux", "devuan", "netbsd", "aperture", "android", "anarchy"
    }
    # Try distro first
    for banner in known_banners:
        if banner in distro:
            return banner
    # Try OS name
    if os_name == "windows":
        return "windows"
    elif os_name == "darwin":
        return "macos"
    elif os_name == "linux":
        return "linux"
    return "normal"