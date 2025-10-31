import sys
import os
import subprocess
import platform
import psutil

from rich.console import Console
from rich.columns import Columns
from rich.text import Text

from src.sys import get_system_info, format_bytes, get_os_banner_name, format_uptime
from asset.banner import *
from __version__ import __version__ as VERSION

console = Console()

def display_system_info():
    info = get_system_info()
    banner_name = get_os_banner_name(info)

    banners = {
        "alter": alter,
        "anarchy": anarchyi,
        "android": android,
        "arch": arch,
        "arch2": arch2,
        "aperture": Aperture,
        "debian": Debian,
        "debian2": Debian2,
        "deepin": Deepin,
        "devuan": Devuan,
        "eurolinux": eurolinux,
        "fedora": Fedora,
        "kali": kali,
        "mint": mint,
        "linux": linux,
        "macos": macos,
        "manjaro": manjaro,
        "netbsd": netbsd,
        "raspberry": raspberry,
        "redhat": redhat,
        "redhat2": redhat2,
        "steamos": steamos,
        "steamos2": steamos2,
        "ubuntu": ubuntu,
        "vanilla": vanilla,
        "windowsserver": windowsserver,
        "windows": windows,
        "normal": normalbn,
        "normal2": normalbn2,
        "normal3": normalbn3,
        "normal4": normalbn4,
        "stars": starsbn,
        "camal": Camalbn,
    }

    colors = {
        "alter": altercolor,
        "anarchy": anarchycolor,
        "android": androidcolor,
        "arch": archcolor,
        "arch2": archcolor,
        "aperture": Aperturecolor,
        "debian": debiancolor,
        "debian2": debiancolor,
        "deepin": deepincolor,
        "devuan": devuancolor,
        "eurolinux": eurolinuxcolor,
        "fedora": fedoracolor,
        "kali": kalicolor,
        "mint": mintcolor,
        "linux": linuxcolor,
        "macos": macoscolor,
        "manjaro": manjarocolor,
        "netbsd": netbsdcolor,
        "raspberry": raspberrycolor,
        "redhat": redhatcolor,
        "redhat2": redhatcolor,
        "steamos": steamoscolor,
        "steamos2": steamoscolor,
        "ubuntu": ubuntucolor,
        "vanilla": vanillacolor,
        "windowsserver": windowsservercolor,
        "windows": windowscolor,
        "normal": normalcolor,
        "normal2": normalcolor,
        "normal3": normalcolor,
        "normal4": normalcolor,
        "stars": normalcolor,
        "camal": normalcolor,
    }
    color_palette = colors.get(banner_name, normalcolor)
    banner_text = banners.get(banner_name, normalbn)
    # color pallette rows
    row1 = "".join(f"[{color_palette[i]}]███[/]" for i in range(0, 8))
    row2 = "".join(f"[{color_palette[i]}]███[/]" for i in range(8, 16))

    # Prepare banner as list of Text objects (with markup)
    if isinstance(banner_text, Text):
        banner_lines = banner_text.split("\n")
    else:
        banner_lines = str(banner_text).splitlines()
    # Calculate max banner width (without markup)
    banner_plain_lines = [line.plain if isinstance(line, Text) else Text.from_markup(line).plain for line in banner_lines]
    
    banner_width = max(len(line) for line in banner_plain_lines) if banner_plain_lines else 0
    gap = 6

    info_lines = []
    info_lines.append(f"[bold cyan]{info.get('user','')}[/bold cyan]@[bold cyan]{info.get('hostname','')}[/bold cyan]")
    info_lines.append("-----")
    os_name = info.get('distro', info.get('os', ''))
    os_name = ""
    if info['os'] == 'Windows':
        os_name = info.get('windows_edition', f"Windows {info.get('os_release', '')}")
    elif info['os'] == 'Linux':
        os_name = info.get('distro', 'Linux')
        if info.get('distro_version'):
            os_name += f" {info['distro_version']}"
    elif info['os'] == 'Darwin':
        os_name = info.get('distro', f"macOS {platform.mac_ver()[0] if 'mac_ver' in dir(platform) else ''}")
    else:
        os_name = info.get('os', 'Unknown')

    # Add architecture
    architecture = info.get('architecture', '')
    if architecture:
        os_name += f" {architecture}"

    info_lines.append(f"[#F9F1A5][bold]OS:[/bold][/#F9F1A5] {os_name}")
    
    # Host information - Motherboard detection
    host_info = None
    if info.get('os') == 'Windows':
        try:
            # Get motherboard product name
            result = subprocess.run(['wmic', 'baseboard', 'get', 'product', '/format:list'],
                                capture_output=True, text=True, check=True, timeout=5)
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.startswith('Product='):
                    host_info = line.split('=', 1)[1].strip()
                    break
            
            # Fallback to computer model
            if not host_info:
                result = subprocess.run(['wmic', 'computersystem', 'get', 'model', '/format:list'],
                                    capture_output=True, text=True, check=True, timeout=5)
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.startswith('Model='):
                        host_info = line.split('=', 1)[1].strip()
                        break
            
            # Clean up the host info
            if host_info:
                host_info = host_info.replace('\x00', '').strip()
                if 'To be filled by O.E.M.' in host_info:
                    host_info = host_info.replace('To be filled by O.E.M.', '').strip()
                
        except Exception as e:
            host_info = None

    if host_info:
        info_lines.append(f"[#F9F1A5][bold]Host:[/bold][/#F9F1A5] {host_info}")
    else:
        # For Linux and other systems, use the hostname as fallback
        info_lines.append(f"[#F9F1A5][bold]Host:[/bold][/#F9F1A5] {info.get('hostname', 'Unknown')}")

    if info['os'] == "Windows":
        info_lines.append(
            f"[#F9F1A5][bold]Kernel:[/bold][/#F9F1A5] {info.get('os_release','')} {info.get('os_version','')}"
        )
    else:
        kernel_full = info.get('os_release', '')
        kernel_extra = info.get('os_version', '')
        if kernel_extra and kernel_extra not in kernel_full:
            kernel_full = f"{kernel_full} {kernel_extra}"
        info_lines.append(
            f"[#F9F1A5][bold]Kernel:[/bold][/#F9F1A5] {kernel_full}"
        )

    info_lines.append(f"[#F9F1A5][bold]Uptime:[/bold][/#F9F1A5] {format_uptime(info.get('uptime', 0))}")

    shell_name = os.path.basename(info['shell']) if info['shell'] != 'Unknown' else 'Unknown'
    if shell_name and shell_name != 'Unknown':
        info_lines.append(f"[#F9F1A5][bold]Shell:[/bold][/#F9F1A5] {shell_name}")

    fonts = info.get('fonts', {})
    system_font = fonts.get('system', '')
    if system_font and system_font != 'Unknown':
        info_lines.append(f"[#F9F1A5][bold]Font:[/bold][/#F9F1A5] {system_font}")

    term_detailed = info.get('terminal_detailed', {})
    term_font = term_detailed.get('font', '')

    if term_font and term_font != 'Unknown':
        info_lines.append(f"[#F9F1A5][bold]Terminal Font:[/bold][/#F9F1A5] {term_font}")

    term_detailed = info.get('terminal_detailed', {})
    term_name = term_detailed.get('name', '')
    term_version = term_detailed.get('version', '')
    term_font = term_detailed.get('font', '')

    if term_name and term_name != 'Unknown':
        term_line = f"[#F9F1A5][bold]Terminal:[/bold][/#F9F1A5] {term_name}"
        if term_version and term_version != 'Unknown':
            term_line += f" {term_version}"
        info_lines.append(term_line)

    display = info.get('display', {})
    displays = display.get('displays', [])

    if not displays:
        info_lines.append("[#F9F1A5][bold]Display:[/bold][/#F9F1A5] No displays detected")
    else:
        for i, disp in enumerate(displays):
            name = disp.get('name', 'Unknown')
            resolution = disp.get('resolution', 'Unknown')
            size = disp.get('size', 'Unknown')
            
            if i == 0:
                info_lines.append(f"[#F9F1A5][bold]Display:[/bold][/#F9F1A5] {name}")
                if size != 'Unknown':
                    info_lines[-1] += f" ({size})"
            else:
                display_line = f"         {name}: {resolution}"
                if size != 'Unknown':
                    display_line += f" ({size})"
                info_lines.append(display_line)

    if info.get('os') == 'Linux':
        info_lines.append(f"[#F9F1A5][bold]DE:[/bold][/#F9F1A5] {info.get('desktop_env','Unknown')}")
        info_lines.append(f"[#F9F1A5][bold]WM:[/bold][/#F9F1A5] {info.get('window_manager','Unknown')}")

    cpu_name = info.get('processor','Unknown')
    cpu_name = info.get('processor', 'Unknown')

    if info.get('os') == 'Windows':
        try:
            result = subprocess.run(['wmic', 'cpu', 'get', 'name', '/format:list'], 
                                capture_output=True, text=True, check=True, timeout=5)
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.startswith('Name='):
                    cpu_name = line.split('=', 1)[1].strip()
                    cpu_name = cpu_name.replace('(R)', '').replace('(TM)', '').replace('(tm)', '')
                    cpu_name = cpu_name.replace('  ', ' ').strip()
                    break
        except Exception:
            pass

    try:
        cpu_cores = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            freq_str = f" @ {cpu_freq.current/1000:.2f} GHz"
        else:
            freq_str = ""
    except Exception:
        cpu_cores = "Unknown"
        freq_str = ""

    if cpu_cores != "Unknown":
        info_lines.append(f"[#F9F1A5][bold]CPU:[/bold][/#F9F1A5] {cpu_name} ({cpu_cores} cores){freq_str}")
    
    elif info.get('os') == 'Linux':
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
                for line in cpuinfo.split('\n'):
                    if line.startswith('model name'):
                        cpu_name = line.split(':', 1)[1].strip()
                        break
        except Exception:
            pass
    else:
        info_lines.append(f"[#F9F1A5][bold]CPU:[/bold][/#F9F1A5] {cpu_name}{freq_str}")

    gpus = info.get('gpu', [])
    for i, gpu in enumerate(gpus):
        prefix = "[#F9F1A5][bold]GPU:[/bold][/#F9F1A5]" if i == 0 else "     "
        info_lines.append(f"{prefix} {gpu}")

    mem = info.get('memory', {})
    info_lines.append(f"[#F9F1A5][bold]Memory:[/bold][/#F9F1A5] {format_bytes(mem.get('used',0))} / {format_bytes(mem.get('total',0))} ({mem.get('percent',0):.1f}%)")

    swap = info.get('swap', {})
    if swap.get('total',0) > 0:
        info_lines.append(f"[#F9F1A5][bold]Swap:[/bold][/#F9F1A5] {format_bytes(swap.get('used',0))} / {format_bytes(swap.get('total',0))} ({swap.get('percent',0):.1f}%)")

    if info.get('os') == 'Windows':
        for disk in info.get('disks', []):
            if disk.get('total',0) > 0:
                info_lines.append(f"[#F9F1A5][bold]Disk ({disk.get('device','')}):[/bold][/#F9F1A5] {format_bytes(disk.get('used',0))} / {format_bytes(disk.get('total',0))} ({disk.get('percent',0):.1f}%) - {disk.get('fstype','')}")

    for iface, addrs in info.get('ip_addresses', {}).items():
        for addr in addrs:
            if not addr.startswith('127.') and not addr.startswith('::1'):
                info_lines.append(f"[#F9F1A5][bold]Local IP ({iface}):[/bold][/#F9F1A5] {addr}")

    info_lines.append(f"[#F9F1A5][bold]OpenRecon:[/bold][/#F9F1A5] {VERSION}")
    locale = info.get('locale', 'Unknown')
    if locale != 'Unknown':
        if len(locale) > 30:
            locale = locale.split()[0]
        info_lines.append(f"[#F9F1A5][bold]Locale:[/bold][/#F9F1A5] {locale}")
    info_lines.append("")
    info_lines.append(row1)
    info_lines.append(row2)

    term_width = console.size.width

    info_width = max(len(Text.from_markup(line).plain) for line in info_lines)
    required_width = banner_width + gap + info_width + 2  # buffer

    if term_width < required_width:
        # Print vertically if not enough horizontal space
        for line in banner_lines:
            if isinstance(line, Text):
                console.print(line)
            else:
                console.print(Text.from_markup(line))
        console.print()
        for line in info_lines:
            console.print(Text.from_markup(line))
    else:
        # Print side by side
        info_rich = [Text.from_markup(line) for line in info_lines]
        max_lines = max(len(banner_lines), len(info_rich))
        banner_rich = []
        for i in range(max_lines):
            if i < len(banner_lines):
                line = banner_lines[i]
                if isinstance(line, Text):
                    plain_length = len(line.plain)
                    if plain_length < banner_width:
                        line += Text(" " * (banner_width - plain_length))
                    banner_rich.append(line)
                else:
                    plain_length = len(Text.from_markup(line).plain)
                    padded_line = line + " " * (banner_width - plain_length)
                    banner_rich.append(Text.from_markup(padded_line))
            else:
                banner_rich.append(Text(" " * banner_width))
        info_rich += [Text("")] * (max_lines - len(info_rich))
        for i in range(max_lines):
            console.print(Text.assemble(banner_rich[i], Text(" " * gap), info_rich[i]))
    print("")

if __name__ == "__main__":
    display_system_info()