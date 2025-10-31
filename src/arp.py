from scapy.all import ARP, Ether, srp, conf
import ipaddress
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import sys
import re
from mac_vendor_lookup import MacLookup
import colorama
from colorama import init, Fore, Style
init(autoreset=True)

import os
import threading
from collections import defaultdict

class ARPDiscovery:
    def __init__(self, timeout=2, max_workers=100, rate_limit=50, retry=1):
        self.timeout = timeout
        self.max_workers = max_workers
        self.rate_limit = rate_limit
        self.retry = retry
        self.found_hosts = {}
        self.monitoring = False
        self.monitor_callback = None
        self.history = defaultdict(list)
        
        # Initialize MAC lookup
        try:
            self.mac_lookup = MacLookup()
        except Exception as e:
            print(f"{Fore.YELLOW}[!] MAC vendor lookup initialization warning: {e}{Style.RESET_ALL}")
            self.mac_lookup = None
        
        conf.verb = 0  # Reduce Scapy output
        
    def get_mac_vendor(self, mac):
        """Get vendor information for a MAC address using mac_vendor_lookup library"""
        if not mac or len(mac) < 8:
            return "Unknown"
        
        if self.mac_lookup is None:
            return "Unknown (Lookup unavailable)"
        
        try:
            # Clean and normalize MAC address
            mac_clean = mac.upper().replace('-', ':')
            vendor = self.mac_lookup.lookup(mac_clean)
            return vendor if vendor else "Unknown Vendor"
        except Exception as e:
            # If lookup fails, return unknown
            return "Unknown Vendor"
        
    def get_ip_type(self, ip, mac):
        now = time.time()
        record = self.history.get(ip, [])

        if len(record) < 2:
            if ip.endswith(".1") or ip.endswith(".254"):
                return "Static"
            return "Dynamic"

        events = record[-5:]
        appeared_events = [e for e in events if e[0] == 'appeared']
        disappeared_events = [e for e in events if e[0] == 'disappeared']

        if len(appeared_events) == 1 and not disappeared_events:
            first_seen = appeared_events[0][1]
            if now - first_seen > 600:
                return "Static"

        if len(appeared_events) > 1 or disappeared_events:
            return "Dynamic"

        return "Unknown"
        
    def get_network_info(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
            
            interface = conf.iface
            return local_ip, interface
            
        except Exception as e:
            print(f"Error getting network info: {e}")
            return None, None
    
    def create_arp_requests(self, ip_range, interface_ip):
        packets = []
        for ip in ip_range:
            arp_request = ARP(pdst=str(ip), psrc=interface_ip)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp_request
            packets.append(packet)
        return packets
    
    def scan_chunk(self, packets_chunk):
        try:
            answered, unanswered = srp(packets_chunk, 
                                     timeout=self.timeout, 
                                     retry=self.retry, 
                                     verbose=False)
            
            results = {}
            for sent, received in answered:
                results[received.psrc] = {
                    'mac': received.hwsrc,
                    'timestamp': time.time()
                }
            return results
            
        except Exception as e:
            print(f"Scan error: {e}")
            return {}
    
    def scan_network(self, network, interface_ip):
        print(f"[*] Scanning {network}...")
        
        network_obj = ipaddress.IPv4Network(network, strict=False)
        ips_to_scan = [str(ip) for ip in network_obj.hosts()]
        
        if not ips_to_scan:
            ips_to_scan = [str(network_obj.network_address)]
        
        print(f"[*] Targeting {len(ips_to_scan)} hosts...")
        
        packets = self.create_arp_requests(ips_to_scan, interface_ip)
        
        chunk_size = max(1, len(packets) // self.max_workers)
        chunks = [packets[i:i + chunk_size] for i in range(0, len(packets), chunk_size)]
        
        print(f"[*] Using {len(chunks)} chunks with {chunk_size} packets each")
        
        start_time = time.time()
        completed = 0
        
        with ThreadPoolExecutor(max_workers=min(len(chunks), self.max_workers)) as executor:
            future_to_chunk = {
                executor.submit(self.scan_chunk, chunk): i 
                for i, chunk in enumerate(chunks)
            }
            
            for future in as_completed(future_to_chunk):
                chunk_id = future_to_chunk[future]
                try:
                    chunk_results = future.result()
                    self.found_hosts.update(chunk_results)
                    completed += 1
                    
                    progress = (completed / len(chunks)) * 100
                    print(f"[*] Progress: {completed}/{len(chunks)} chunks ({progress:.1f}%) - Found {len(self.found_hosts)} hosts so far")
                    
                except Exception as e:
                    print(f"Chunk {chunk_id} failed: {e}")
        
        return time.time() - start_time
    
    def scan_single_batch(self, network, interface_ip):
        print(f"[*] Scanning {network} in single batch...")
        
        arp_request = ARP(pdst=network, psrc=interface_ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp_request
        
        start_time = time.time()
        
        answered, unanswered = srp(packet, 
                                 timeout=self.timeout, 
                                 retry=self.retry, 
                                 verbose=False)
        
        scan_time = time.time() - start_time
        
        for sent, received in answered:
            self.found_hosts[received.psrc] = {
                'mac': received.hwsrc,
                'timestamp': time.time()
            }
        
        return scan_time
    
    def scan(self, network=None, interface=None):
        print("[*] Starting ARP discovery with Scapy...")
        
        interface_ip, default_interface = self.get_network_info()
        
        if not interface_ip:
            print("[-] Could not determine network configuration")
            return
        
        scan_interface = interface or default_interface
        
        if network:
            try:
                target_network = str(ipaddress.IPv4Network(network, strict=False))
            except ValueError as e:
                print(f"[-] Invalid network format: {e}")
                return
        else:
            network_addr = '.'.join(interface_ip.split('.')[:3]) + '.0/24'
            target_network = network_addr
        
        print(f"[*] Interface IP: {interface_ip}")
        print(f"[*] Network interface: {scan_interface}")
        print(f"[*] Target network: {target_network}")
        print(f"[*] Workers: {self.max_workers}, Timeout: {self.timeout}s")
        print(f"[*] Rate limit: {self.rate_limit} pps, Retry: {self.retry}")
        print("-" * 50)
        
        if scan_interface:
            conf.iface = scan_interface
        
        network_obj = ipaddress.IPv4Network(target_network, strict=False)
        host_count = len(list(network_obj.hosts())) or 1
        
        if host_count > 1000 and self.max_workers > 1:
            print("[*] Using chunked parallel scanning (large network)")
            scan_time = self.scan_network(target_network, interface_ip)
        else:
            print("[*] Using single batch scanning")
            scan_time = self.scan_single_batch(target_network, interface_ip)
        
        print(f"\n[+] Scan completed in {scan_time:.2f} seconds")
        print(f"[+] Found {len(self.found_hosts)} active hosts:")
        print("-" * 50)
        for ip in sorted(self.found_hosts.keys()):
            info = self.found_hosts[ip]
            vendor = self.get_mac_vendor(info['mac'])
            print(f"{ip:15} -> {info['mac']:17} | {vendor}")
        
        return self.found_hosts

    def _monitor_cycle(self, network, interface_ip, interval, callback):
        previous_hosts = self.found_hosts.copy()

        network_obj = ipaddress.IPv4Network(network, strict=False)
        host_count = len(list(network_obj.hosts())) or 1

        if host_count > 1000 and self.max_workers > 1:
            scan_time = self.scan_network(network, interface_ip)
        else:
            scan_time = self.scan_single_batch(network, interface_ip)

        current_scan_results = self.found_hosts.copy()

        new_hosts = {ip: info for ip, info in current_scan_results.items() if ip not in previous_hosts}
        gone_hosts = {ip: info for ip, info in previous_hosts.items() if ip not in current_scan_results}

        timestamp = time.time()
        for ip in new_hosts:
            self.history[ip].append(('appeared', timestamp))
        for ip in gone_hosts:
            self.history[ip].append(('disappeared', timestamp))

        if callback and (new_hosts or gone_hosts):
            try:
                callback(new_hosts, gone_hosts, current_scan_results)
            except Exception:
                pass

        return new_hosts, gone_hosts, scan_time


    def start_monitoring(self, network=None, interface=None, interval=30, callback=None):
        interface_ip, default_interface = self.get_network_info()
        if not interface_ip:
            print(f"{Fore.RED}[-] Could not determine network configuration{Style.RESET_ALL}")
            return

        scan_interface = interface or default_interface
        
        interface_str = str(scan_interface) if scan_interface else "Unknown"

        if network:
            try:
                target_network = str(ipaddress.IPv4Network(network, strict=False))
            except ValueError as e:
                print(f"{Fore.RED}[-] Invalid network format: {e}{Style.RESET_ALL}")
                return
        else:
            network_addr = '.'.join(interface_ip.split('.')[:3]) + '.0/24'
            target_network = network_addr

        if scan_interface:
            conf.iface = scan_interface

        self.monitoring = True
        self.monitor_callback = callback
        cycle_count = 0

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"[*] Target: {target_network}")
        print(f"[*] Interface: {interface_str}")
        print(f"[*] Interval: {interval}s")
        print(f"\nPress {Fore.YELLOW}Ctrl+C{Style.RESET_ALL} to stop monitoring...\n")

        try:
            while self.monitoring:
                cycle_count += 1
                cycle_start = time.time()

                new_hosts, gone_hosts, scan_time = self._monitor_cycle(
                    target_network, interface_ip, interval, callback
                )

                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"[*] Target: {target_network}")
                print(f"[*] Interface: {interface_str}")
                print(f"[*] Interval: {interval}s")

                ts = time.strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{ts}] Cycle #{cycle_count} — Scan time: {scan_time:.2f}s | Active: {len(self.found_hosts)} | New: {len(new_hosts)} | Left: {len(gone_hosts)}\n")

                if self.found_hosts:
                    print("Active hosts:")
                    for ip in sorted(self.found_hosts.keys()):
                        info = self.found_hosts[ip]
                        mac = info.get('mac', 'Unknown')
                        vendor = self.get_mac_vendor(mac)
                        ip_type = self.get_ip_type(ip, mac)
                        color = Fore.GREEN if ip in new_hosts else ""
                        
                        if ip in new_hosts:
                            print(f"  {Fore.GREEN}[+] {ip:15} -> {mac:17} | {ip_type} | {vendor:30} {Style.RESET_ALL}")
                        else:
                            print(f"  {ip:15} -> {mac:17} | {ip_type} | {vendor:30}")
                else:
                    print(f"  {Fore.YELLOW}[=] No active hosts found{Style.RESET_ALL}")

                if gone_hosts:
                    print("")
                    for ip, info in sorted(gone_hosts.items()):
                        mac = info.get('mac', 'unknown')
                        vendor = self.get_mac_vendor(mac)
                        print(f"  {Fore.RED}[-] {ip:15} -> {mac:17} | {vendor:30} | LEFT{Style.RESET_ALL}")

                if not new_hosts and not gone_hosts:
                    print(f"\n{Fore.YELLOW}[=] No changes detected this cycle{Style.RESET_ALL}")

                elapsed = time.time() - cycle_start
                wait_time = max(0, interval - int(elapsed))
                print(f"\n[*] Cycle completed in {elapsed:.2f}s — next scan in {wait_time}s")

                # Wait for the remaining interval time
                wait_time = 0
                while wait_time < interval and self.monitoring:
                    time.sleep(1)
                    wait_time += 1

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Monitoring stopped by user{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] Monitoring error: {e}{Style.RESET_ALL}")
        finally:
            self.monitoring = False
            print(f"{Fore.CYAN}[*] ARP monitoring stopped{Style.RESET_ALL}")

    def stop_monitoring(self):
        self.monitoring = False
        print("[*] Stopping ARP monitoring...")

    def get_host_history(self, ip):
        return self.history.get(ip, [])

def custom_monitor_callback(new_hosts, gone_hosts, current_hosts):
    if new_hosts or gone_hosts:
        print(f"\n[!] Network change detected at {time.strftime('%H:%M:%S')}:")
        if new_hosts:
            print(f"    [+] New devices: {', '.join(sorted(new_hosts.keys()))}")
        if gone_hosts:
            print(f"    [-] Gone devices: {', '.join(sorted(gone_hosts.keys()))}")

def main():
    parser = argparse.ArgumentParser(description='ARP Discovery Scanner with Scapy')
    parser.add_argument('-n', '--network', help='Target network (e.g., 192.168.1.0/24)')
    parser.add_argument('-i', '--interface', help='Network interface to use')
    parser.add_argument('-t', '--timeout', type=int, default=2, help='Scan timeout in seconds')
    parser.add_argument('-w', '--workers', type=int, default=50, help='Number of concurrent workers')
    parser.add_argument('-r', '--rate', type=int, default=100, help='Rate limit (packets per second)')
    parser.add_argument('--retry', type=int, default=1, help='Number of retries')
    
    # Monitoring options
    parser.add_argument('-m', '--monitor', action='store_true', help='Enable continuous monitoring mode')
    parser.add_argument('--interval', type=int, default=30, help='Monitoring interval in seconds')
    
    args = parser.parse_args()
    
    
    scanner = ARPDiscovery(
        timeout=args.timeout, 
        max_workers=args.workers, 
        rate_limit=args.rate,
        retry=args.retry
    )
    
    try:
        if args.monitor:
            scanner.start_monitoring(
                network=args.network, 
                interface=args.interface, 
                interval=args.interval,
                callback=custom_monitor_callback
            )
        else:
            scanner.scan(network=args.network, interface=args.interface)
    except KeyboardInterrupt:
        if args.monitor:
            scanner.stop_monitoring()
        else:
            print("\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"[-] Operation failed: {e}")
        if "root" in str(e).lower() or "permission" in str(e).lower():
            print("\nNote: you may need to run with administrator privileges")
            print("or adjust system settings to allow raw socket access.")

if __name__ == "__main__":
    main()