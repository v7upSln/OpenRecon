import argparse
import sys
import os
import subprocess
from pathlib import Path

SCRIPT_DIR = "src"

def get_script_path(script_name):
    script_path = os.path.join(SCRIPT_DIR, script_name)
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"[!] Script '{script_name}' not found in '{SCRIPT_DIR}' directory.")
    return script_path

def display_system_info():
    try:
        from info import display_system_info as show_info
        show_info()
        return 0
    except ImportError as e:
        print(f"Error: Could not import system info module: {e}")
        return 1
    except Exception as e:
        print(f"Error displaying system information: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser(
        description='OpenRecon: A network reconnaissance tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        title='available commands',
        description='choose one of the following scanning methods',
        help='additional help with [command] -h'
    )
    
    # ARP Discovery Parser
    arp_parser = subparsers.add_parser('arp', help='ARP network discovery and monitoring')
    arp_parser.add_argument('-n', '--network', help='Target network (e.g., 192.168.1.0/24)')
    arp_parser.add_argument('-i', '--interface', help='Network interface to use')
    arp_parser.add_argument('-t', '--timeout', type=int, default=2, help='Scan timeout in seconds')
    arp_parser.add_argument('-w', '--workers', type=int, default=50, help='Number of concurrent workers')
    arp_parser.add_argument('-r', '--rate', type=int, default=100, help='Rate limit (packets per second)')
    arp_parser.add_argument('--retry', type=int, default=1, help='Number of retries')
    arp_parser.add_argument('-m', '--monitor', action='store_true', help='Enable continuous monitoring mode')
    arp_parser.add_argument('--interval', type=int, default=30, help='Monitoring interval in seconds')
    
    # Packet Grabber Parser
    packet_parser = subparsers.add_parser('packetgrab', help='Packet sniffing and analysis')
    packet_parser.add_argument('-i', '--interface', help='Network interface to sniff on')
    packet_parser.add_argument('-c', '--count', type=int, default=0, help='Number of packets to capture (0 = unlimited)')
    packet_parser.add_argument('-f', '--filter', dest='filter_protocol', help='BPF filter (e.g., "tcp", "udp port 53", "host 192.168.1.1")')
    packet_parser.add_argument('-o', '--output', help='Save packets to file (text log) or .pcap to save capture')
    packet_parser.add_argument('-l', '--list', action='store_true', help='List available network interfaces')
    packet_parser.add_argument('--verbose', action='store_true', help='Print full HTTP bodies and larger payloads')
    packet_parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    packet_parser.add_argument('--max-payload-length', type=int, default=2048, help='Max bytes of body to show when not verbose')
    
    # Ping Sweep Parser
    ping_parser = subparsers.add_parser('ping', help='ICMP ping sweep')
    ping_parser.add_argument('prefix', help='IP prefix (e.g. 192.168.1 or 192.168.1.0/24)')
    ping_parser.add_argument('--start', type=int, default=1, help='start host (default 1)')
    ping_parser.add_argument('--end', type=int, default=254, help='end host (default 254)')
    ping_parser.add_argument('-t', '--timeout', type=float, default=1.0, help='per-ping timeout in seconds (default 1.0)')
    ping_parser.add_argument('-c', '--concurrency', type=int, default=20, help='max concurrent pings (default 20)')
    ping_parser.add_argument('-r', '--rate', type=float, default=50.0, help='max pings per second (default 50)')
    
    # Port Scan Parser
    port_parser = subparsers.add_parser('portscan', help='TCP port scanning with WAF detection')
    port_parser.add_argument('target', help='Target IP or domain to scan')
    port_parser.add_argument('-p', '--ports', help='Ports to scan (e.g., 80,443 or 1-1000)')
    port_parser.add_argument('-t', '--threads', type=int, default=1000, help='Number of threads (default: 1000)')
    port_parser.add_argument('-c', '--common', action='store_true', help='Scan common ports only')
    port_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    port_parser.add_argument('--nmap', action='store_true', help='Run nmap version detection on open ports')
    port_parser.add_argument('--banner', action='store_true', help='Attempt banner grabbing')
    port_parser.add_argument('--waf', action='store_true', help='Enable WAF detection')
    port_parser.add_argument('--nowaf', action='store_true', help='Disable WAF detection')
    
    args = parser.parse_args()
    
    # If no command is provided, display system info
    if not args.command:
        return display_system_info()
    
    script_map = {
        'arp': 'arp.py',
        'packetgrab': 'packetgrab.py',
        'ping': 'pingsweep.py',
        'portscan': 'portscan.py'
    }
    
    try:
        script_file = get_script_path(script_map[args.command])
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"\nMake sure all script files are in the '{SCRIPT_DIR}' directory:")
        print("  - arp.py")
        print("  - packetgrab.py") 
        print("  - pingsweep.py")
        print("  - portscan.py")
        return 1
    
    # Build command based on the selected tool
    cmd = [sys.executable, script_file]
    
    if args.command == 'arp':
        if args.network: cmd.extend(['-n', args.network])
        if args.interface: cmd.extend(['-i', args.interface])
        if args.timeout: cmd.extend(['-t', str(args.timeout)])
        if args.workers: cmd.extend(['-w', str(args.workers)])
        if args.rate: cmd.extend(['-r', str(args.rate)])
        if args.retry: cmd.extend(['--retry', str(args.retry)])
        if args.monitor:
            cmd.extend(['-m'])
            if args.interval: cmd.extend(['--interval', str(args.interval)])
        
    elif args.command == 'packetgrab':
        if args.interface: cmd.extend(['-i', args.interface])
        if args.count: cmd.extend(['-c', str(args.count)])
        if args.filter_protocol: cmd.extend(['-f', args.filter_protocol])
        if args.output: cmd.extend(['-o', args.output])
        if args.list: cmd.extend(['-l'])
        if args.verbose: cmd.extend(['--verbose'])
        if args.no_color: cmd.extend(['--no-color'])
        if args.max_payload_length: cmd.extend(['--max-payload-length', str(args.max_payload_length)])
        
    elif args.command == 'ping':
        cmd.append(args.prefix)
        if args.start: cmd.extend(['--start', str(args.start)])
        if args.end: cmd.extend(['--end', str(args.end)])
        if args.timeout: cmd.extend(['-t', str(args.timeout)])
        if args.concurrency: cmd.extend(['-c', str(args.concurrency)])
        if args.rate: cmd.extend(['-r', str(args.rate)])
        
    elif args.command == 'portscan':
        cmd.append(args.target)
        if args.ports: cmd.extend(['-p', args.ports])
        if args.threads: cmd.extend(['-t', str(args.threads)])
        if args.common: cmd.extend(['-c'])
        if args.verbose: cmd.extend(['-v'])
        if args.nmap: cmd.extend(['--nmap'])
        if args.banner: cmd.extend(['--banner'])
        if args.waf: cmd.extend(['--waf'])
        if args.nowaf: cmd.extend(['--nowaf'])
    
    try:
        print(f"[*] Executing: {' '.join(cmd)}")
        print("-" * 80)
        result = subprocess.run(cmd)
        return result.returncode
    except KeyboardInterrupt:
        print("\n[!] Operation interrupted by user")
        return 1
    except Exception as e:
        print(f"[!] Error executing command: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())