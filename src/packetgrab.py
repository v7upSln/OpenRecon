from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP, Ether, Raw, get_if_list, wrpcap, AsyncSniffer
from scapy.layers.http import HTTPRequest, HTTPResponse
import argparse
import sys
from datetime import datetime
from collections import defaultdict
import os
import io
import gzip
import zlib
import re

try:
    from colorama import Fore, Style, init as colorama_init
    COLORAMA_AVAILABLE = True
    colorama_init(autoreset=True)
except Exception:
    COLORAMA_AVAILABLE = False
    class _Fake:
        RESET = ''
    Fore = Style = _Fake()

class Colors:
    HTTP = getattr(Fore, 'YELLOW', '\033[93m')
    TCP = getattr(Fore, 'BLUE', '\033[94m')
    UDP = getattr(Fore, 'CYAN', '\033[96m')
    ARP = getattr(Fore, 'MAGENTA', '\033[95m')
    ICMP = getattr(Fore, 'RED', '\033[91m')
    ETHER = getattr(Fore, 'WHITE', '\033[97m')
    PAYLOAD = getattr(Fore, 'GREEN', '\033[92m')
    RESET = getattr(Style, 'RESET_ALL', '\033[0m')
    BOLD = getattr(Style, 'BRIGHT', '')

def dechunk_http_body(chunked: bytes) -> bytes:
    out = bytearray()
    s = memoryview(chunked)
    i = 0
    while i < len(s):
        j = bytes(s[i:]).find(b'\r\n')
        if j == -1:
            break
        line = bytes(s[i:i+j]).decode('ascii', errors='ignore').strip()
        try:
            length = int(line.split(';', 1)[0], 16)
        except ValueError:
            break
        i += j + 2
        if length == 0:
            break
        out += s[i:i+length]
        i += length + 2
    return bytes(out)

def decompress_body(body_bytes: bytes, encoding: str) -> bytes:
    try:
        if encoding == 'gzip':
            return gzip.decompress(body_bytes)
        if encoding in ('deflate', 'zlib'):
            try:
                return zlib.decompress(body_bytes)
            except Exception:
                # raw deflate
                return zlib.decompress(body_bytes, -zlib.MAX_WBITS)
    except Exception:
        pass
    return body_bytes

class PacketSniffer:
    def __init__(self, interface=None, count=0, filter_protocol=None, output_file=None,verbose=False, use_color=True, max_payload=2048):
        self.interface = interface
        self.count = count
        self.filter_protocol = filter_protocol
        self.output_file = output_file
        self.packet_count = 0
        self.protocol_stats = defaultdict(int)
        self.verbose = verbose
        self.use_color = use_color and (COLORAMA_AVAILABLE or 'TERM' in os.environ)
        self.max_payload = max_payload
        self._pcap_packets = [] if (output_file and output_file.lower().endswith('.pcap')) else None
        self._log_fd = None
        if output_file and not self._pcap_packets:
            self._log_fd = open(output_file, 'a', buffering=1, encoding='utf-8', errors='ignore')

    def __del__(self):
        if self._log_fd:
            try:
                self._log_fd.close()
            except Exception:
                pass

    def _color(self, color_code):
        return color_code if self.use_color else ''

    def packet_handler(self, packet):
        self.packet_count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        color = self._color(Colors.ETHER)
        is_http = False

        sep = '=' * 80
        print(f"\n{color}{sep}{self._color(Colors.RESET)}")
        print(f"{color}[Packet #{self.packet_count}] {timestamp}{self._color(Colors.RESET)}")
        print(f"{color}{sep}{self._color(Colors.RESET)}")

        if packet.haslayer(Ether):
            eth = packet[Ether]
            print(f"{self._color(Colors.ETHER)}[Ethernet] Src MAC: {eth.src} -> Dst MAC: {eth.dst}{self._color(Colors.RESET)}")

        if packet.haslayer(ARP):
            arp = packet[ARP]
            self.protocol_stats['ARP'] += 1
            print(f"{self._color(Colors.ARP)}[ARP] Operation: {arp.op} | Src IP: {arp.psrc} -> Dst IP: {arp.pdst}{self._color(Colors.RESET)}")

        ip = packet.getlayer(IP)
        if ip:
            sport = self.get_port(packet, 'src')
            dport = self.get_port(packet, 'dst')
            proto = ip.proto
            print(f"{self._color(Colors.ETHER)}[IP] Src: {ip.src}{(':'+str(sport)) if sport != '' else ''} -> Dst: {ip.dst}{(':'+str(dport)) if dport != '' else ''}")
            print(f"     Protocol: {proto} | TTL: {ip.ttl} | Length: {ip.len}{self._color(Colors.RESET)}")

            if packet.haslayer(TCP):
                tcp = packet[TCP]
                self.protocol_stats['TCP'] += 1
                flags = self.get_tcp_flags(tcp.flags)
                print(f"{self._color(Colors.TCP)}[TCP] Sport: {tcp.sport} -> Dport: {tcp.dport}")
                print(f"      Flags: {flags} | Seq: {tcp.seq} | Ack: {tcp.ack}{self._color(Colors.RESET)}")

                if packet.haslayer(HTTPRequest) or packet.haslayer(HTTPResponse):
                    is_http = True
                    self.protocol_stats['HTTP'] += 1
                    if packet.haslayer(HTTPRequest):
                        http = packet[HTTPRequest]
                        print(f"{self._color(Colors.HTTP)}{Colors.BOLD}[HTTP REQUEST]{self._color(Colors.RESET)}")
                        print(f"{self._color(Colors.HTTP)}{'─'*80}{self._color(Colors.RESET)}")
                        method = getattr(http, 'Method', None)
                        host = getattr(http, 'Host', None)
                        path = getattr(http, 'Path', None)
                        try:
                            method = method.decode() if method else ''
                            host = host.decode() if host else ''
                            path = path.decode() if path else ''
                        except Exception:
                            method = method or ''
                            host = host or ''
                            path = path or ''
                        print(f"{self._color(Colors.HTTP)}Method: {method} | Host: {host} | Path: {path}{self._color(Colors.RESET)}")
                        if packet.haslayer(Raw):
                            self._display_http_payload(packet[Raw].load)
                        print(f"{self._color(Colors.HTTP)}{'─'*80}{self._color(Colors.RESET)}")
                    else:
                        http = packet[HTTPResponse]
                        print(f"{self._color(Colors.HTTP)}{Colors.BOLD}[HTTP RESPONSE]{self._color(Colors.RESET)}")
                        print(f"{self._color(Colors.HTTP)}{'─'*80}{self._color(Colors.RESET)}")
                        if packet.haslayer(Raw):
                            self._display_http_payload(packet[Raw].load)
                        print(f"{self._color(Colors.HTTP)}{'─'*80}{self._color(Colors.RESET)}")

                elif packet.haslayer(Raw):
                    payload = bytes(packet[Raw].load)
                    try:
                        payload_str = payload.decode('utf-8', errors='ignore')
                        first_line = payload_str.split('\r\n', 1)[0]
                        if re.match(r'^(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH) ', first_line) or payload_str.startswith('HTTP/'):
                            self.protocol_stats['HTTP'] += 1
                            is_http = True
                            kind = "REQUEST - Raw" if not payload_str.startswith('HTTP/') else "RESPONSE - Raw"
                            print(f"{self._color(Colors.HTTP)}{Colors.BOLD}[HTTP {kind}]{self._color(Colors.RESET)}")
                            print(f"{self._color(Colors.HTTP)}{'─'*80}{self._color(Colors.RESET)}")
                            self._display_http_payload(payload)
                            print(f"{self._color(Colors.HTTP)}{'─'*80}{self._color(Colors.RESET)}")
                    except Exception:
                        pass

            elif packet.haslayer(UDP):
                udp = packet[UDP]
                self.protocol_stats['UDP'] += 1
                print(f"{self._color(Colors.UDP)}[UDP] Sport: {udp.sport} -> Dport: {udp.dport} | Length: {udp.len}{self._color(Colors.RESET)}")

            elif packet.haslayer(ICMP):
                icmp = packet[ICMP]
                self.protocol_stats['ICMP'] += 1
                print(f"{self._color(Colors.ICMP)}[ICMP] Type: {icmp.type} | Code: {icmp.code}{self._color(Colors.RESET)}")

        if packet.haslayer(Raw) and not is_http:
            payload = bytes(packet[Raw].load)
            if len(payload) > 0:
                hex_preview = ' '.join(f'{b:02x}' for b in payload[:32])
                print(f"{self._color(Colors.PAYLOAD)}[Payload] {len(payload)} bytes | Hex: {hex_preview}...{self._color(Colors.RESET)}")

        if self.output_file:
            if self._pcap_packets is not None:
                self._pcap_packets.append(packet)
            elif self._log_fd:
                try:
                    self._log_fd.write(f"{timestamp} | {packet.summary()}\n")
                except Exception:
                    pass

    def _display_http_payload(self, raw_bytes: bytes):
        headers_part = b''
        body_part = b''
        sep = b'\r\n\r\n'
        idx = raw_bytes.find(sep)
        if idx != -1:
            headers_part = raw_bytes[:idx]
            body_part = raw_bytes[idx+len(sep):]
        else:
            body_part = raw_bytes

        headers_text = ''
        headers = {}
        if headers_part:
            try:
                headers_text = headers_part.decode('iso-8859-1', errors='ignore')
                for line in headers_text.split('\r\n')[1:]:
                    if ':' in line:
                        k, v = line.split(':', 1)
                        headers[k.strip().lower()] = v.strip()
            except Exception:
                headers_text = ''

        transfer_encoding = headers.get('transfer-encoding', '').lower()
        content_encoding = headers.get('content-encoding', '').lower()
        content_type = headers.get('content-type', '').lower()

        if 'chunked' in transfer_encoding:
            try:
                body_part = dechunk_http_body(body_part)
            except Exception:
                pass

        if content_encoding in ('gzip', 'x-gzip', 'deflate', 'zlib'):
            try:
                body_part = decompress_body(body_part, 'gzip' if 'gzip' in content_encoding else 'deflate')
            except Exception:
                pass
        else:
            if len(body_part) >= 2 and body_part[0] == 0x1f and body_part[1] == 0x8b:
                try:
                    body_part = gzip.decompress(body_part)
                except Exception:
                    pass

        is_text = False
        if content_type:
            if any(t in content_type for t in ['text', 'json', 'xml', 'javascript', 'html', 'css']):
                is_text = True
        else:
            try:
                _ = body_part.decode('utf-8')
                is_text = True
            except Exception:
                is_text = False

        if headers_text:
            print(headers_text)

        if len(body_part) == 0:
            print("[HTTP] <no body>")
            return

        if is_text:
            try:
                body_text = body_part.decode('utf-8', errors='replace')
            except Exception:
                body_text = body_part.decode('iso-8859-1', errors='replace')

            if self.verbose:
                to_print = body_text if len(body_text) <= 100000 else body_text[:100000] + "\n...[truncated]"
                print(to_print)
            else:
                if len(body_text) > self.max_payload:
                    print(body_text[:self.max_payload] + "\n...[truncated] (use --verbose to show more)")
                else:
                    print(body_text)
        else:
            print(f"[HTTP-BINARY] {len(body_part)} bytes (binary). Showing hexdump preview:")
            hex_preview = ' '.join(f'{b:02x}' for b in body_part[:64])
            print(hex_preview + (' ...' if len(body_part) > 64 else ''))

    def get_port(self, packet, direction):
        """Return port number (string) or '' if none"""
        if packet.haslayer(TCP):
            return packet[TCP].sport if direction == 'src' else packet[TCP].dport
        if packet.haslayer(UDP):
            return packet[UDP].sport if direction == 'src' else packet[UDP].dport
        return ''

    def get_tcp_flags(self, flags):
        """Return human readable TCP flags (works with Scapy flags)"""
        try:
            flag_str = str(flags)
        except Exception:
            flag_str = ''
        flag_map = {
            'F': 'FIN', 'S': 'SYN', 'R': 'RST',
            'P': 'PSH', 'A': 'ACK', 'U': 'URG',
            'E': 'ECE', 'C': 'CWR'
        }
        return ' '.join(flag_map.get(ch, ch) for ch in flag_str if ch in flag_map)

    def start(self):
        print(f"[*] Interface: {self.interface or 'Default'}")
        print(f"[*] Count: {'Unlimited' if self.count == 0 else self.count}")
        print(f"[*] Filter: {self.filter_protocol or 'All protocols'}")
        print(f"[*] Verbose: {self.verbose}")
        if self.output_file:
            print(f"[*] Output: {self.output_file}")
            if self.output_file.lower().endswith('.pcap'):
                print("  (.pcap mode — Wireshark compatible)")
        print("-"*80)
        print(" Press Ctrl+C to stop\n")

        try:
            if self.output_file and self.output_file.lower().endswith('.pcap'):
                self._async_sniffer = AsyncSniffer(
                    iface=self.interface,
                    filter=self.filter_protocol,
                    store=True,
                    prn=self.packet_handler
                )
                self._async_sniffer.start()
                
                try:
                    if self.count > 0:
                        print(f"[+] Capturing {self.count} packets...")
                        self._async_sniffer.join(timeout=300)
                    else:
                        input("Sniffing... Press Enter or Ctrl+C to stop.\n")
                except KeyboardInterrupt:
                    print("\n[!] Interrupted by user.")
                finally:
                    self._async_sniffer.stop()
                    
                packets = self._async_sniffer.results
                if packets:
                    wrpcap(self.output_file, packets)
                    print(f"\n[+] Wrote {len(packets)} packets to {self.output_file}")
                else:
                    print(f"\n[!] No packets captured for {self.output_file}")
                    
            else:
                sniff(
                    iface=self.interface,
                    prn=self.packet_handler,
                    count=self.count,
                    store=False,
                    filter=self.filter_protocol
                )

        except KeyboardInterrupt:
            print("\nStopping capture...")
        except PermissionError:
            print("\n[ERROR] Permission denied. Run with administrator/root privileges.")
            sys.exit(1)
        except Exception as e:
            print(f"\n[ERROR] {e}")
            sys.exit(1)
        finally:
            self.print_statistics()
        
    def print_statistics(self):
        print("\n" + "-"*80)
        print("[+] CAPTURE STATISTICS")
        print(f" Total Packets: {self.packet_count}")
        print("\n Protocol Breakdown:")
        for proto, count in sorted(self.protocol_stats.items()):
            percentage = (count / self.packet_count * 100) if self.packet_count > 0 else 0
            print(f"   {proto:10s}: {count:6d} packets ({percentage:5.2f}%)")
        print("-"*80 + "\n")

def list_interfaces():
    print("\n[*] Available network interfaces:")
    for i, iface in enumerate(get_if_list(), 1):
        print(f"  {i}. {iface}")
    print()

def main():
    parser = argparse.ArgumentParser(
        description='Packet Sniffer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('-i', '--interface', help='Network interface to sniff on')
    parser.add_argument('-c', '--count', type=int, default=0, help='Number of packets to capture (0 = unlimited)')
    parser.add_argument('-f', '--filter', dest='filter_protocol', help='BPF filter (e.g., "tcp", "udp port 53", "host 192.168.1.1")')
    parser.add_argument('-o', '--output', help='Save packets to file (text log) or .pcap to save capture')
    parser.add_argument('-l', '--list', action='store_true', help='List available network interfaces')
    parser.add_argument('--verbose', action='store_true', help='Print full HTTP bodies and larger payloads')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    parser.add_argument('--max-payload-length', type=int, default=2048, help='Max bytes of body to show when not verbose')

    args = parser.parse_args()

    if args.list:
        list_interfaces()
        sys.exit(0)

    sniffer = PacketSniffer(
        interface=args.interface,
        count=args.count,
        filter_protocol=args.filter_protocol,
        output_file=args.output,
        verbose=args.verbose,
        use_color=not args.no_color,
        max_payload=args.max_payload_length
    )

    sniffer.start()

if __name__ == "__main__":
    main()