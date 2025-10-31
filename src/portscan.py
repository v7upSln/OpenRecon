import socket
import threading
import concurrent.futures
import subprocess
import time
from colorama import Fore, Style, init
import sys
import ipaddress
import argparse
import requests
import urllib3
import re
import ssl
import random
from urllib.parse import urljoin
from collections import defaultdict

# Suppress insecure warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init()

# WAF detection fingerprints
FINGERPRINTS = [
    # Cloudflare
    (r"cloudflare", "Cloudflare", 6, "header"),
    (r"cf-ray", "Cloudflare", 5, "header"),
    (r"__cf_bm", "Cloudflare", 5, "cookie"),
    (r"__cfduid", "Cloudflare", 3, "cookie"),
    (r"cf-cache-status", "Cloudflare", 2, "header"),
    
    # Akamai
    (r"akamai", "Akamai", 5, "header"),
    (r"akamaiedge", "Akamai", 4, "header"),
    (r"x-akamai-transformed", "Akamai", 3, "header"),
    
    # Fastly
    (r"fastly", "Fastly", 4, "header"),
    (r"x-served-by", "Fastly", 2, "header"),
    
    # Imperva / Incapsula
    (r"incapsula", "Imperva/Incapsula", 6, "header"),
    (r"x-iinfo", "Imperva/Incapsula", 4, "header"),
    (r"visid_incap_", "Imperva/Incapsula", 4, "cookie"),
    
    # AWS / ELB hints
    (r"awselb", "AWS (ELB/ALB)", 3, "header"),
    (r"amazon", "AWS (certificate/issuer)", 2, "tls"),
    (r"elasticloadbalancing", "AWS (ELB/ALB)", 3, "header"),
    
    # F5 / BIG-IP
    (r"bigip", "F5 Big-IP", 5, "header"),
    (r"BIGipServer", "F5 Big-IP", 5, "cookie"),
    
    # Sucuri
    (r"sucuri", "Sucuri", 5, "header"),
    (r"x-sucuri-id", "Sucuri", 4, "header"),
    
    # Barracuda
    (r"barracuda", "Barracuda", 4, "header"),
    (r"barracuda-nginx", "Barracuda", 3, "header"),
    
    # Fortinet / FortiWeb
    (r"fortinet", "Fortinet", 4, "header"),
    (r"fortiweb", "Fortinet FortiWeb", 5, "header"),
    (r"FCTOKEN", "Fortinet", 3, "cookie"),
    
    # Palo Alto
    (r"panos", "Palo Alto Networks", 3, "header"),
    
    # Cisco
    (r"cisco", "Cisco", 2, "header"),
    
    # ModSecurity
    (r"mod_security|modsecurity|modsec", "ModSecurity", 5, "header"),
    (r"owasp", "ModSecurity/OWASP-CRS", 3, "body"),
    
    # Wordfence
    (r"wordfence", "Wordfence", 6, "body"),
    (r"wfwaf", "Wordfence", 4, "header"),
    
    # Generic WAF indicators
    (r"access denied|request blocked|your request was blocked|blocked by|forbidden", "Generic WAF", 3, "body"),
    (r"waf", "Generic WAF", 2, "body"),
    (r"web application firewall", "Generic WAF", 3, "body"),
]

# Common paths for WAF detection
COMMON_PATHS = [
    "/", "/index.php", "/login", "/admin", "/wp-login.php", 
    "/robots.txt", "/sitemap.xml"
]

# Payloads for WAF probing
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "'><img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
]

SQLI_PAYLOADS = [
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "' OR 1=1--",
    "' UNION SELECT NULL--",
]

class WAFDetector:
    def __init__(self, target, scheme="http", timeout=6):
        self.target = target
        self.scheme = scheme
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml"
        })
    
    def _make_url(self, port, path="/"):
        if port in (80, 443):
            return f"{self.scheme}://{self.target}{path}"
        else:
            return f"{self.scheme}://{self.target}:{port}{path}"
    
    def _request(self, url, method="GET", data=None):
        try:
            r = self.session.request(
                method, url, 
                timeout=self.timeout, 
                verify=False, 
                allow_redirects=True,
                data=data
            )
            return r
        except requests.RequestException:
            return None
    
    def detect_waf(self):
        """Detect WAF using multiple techniques"""
        results = defaultdict(int)
        evidence = []
        
        # Test common web ports
        test_ports = [80, 443, 8080, 8443]
        
        for port in test_ports:
            # Test normal request first
            url = self._make_url(port, "/")
            normal_response = self._request(url)
            
            if not normal_response:
                continue
                
            # Check for WAF fingerprints in headers and body
            self._check_fingerprints(normal_response, results, evidence)
            
            # Test with malicious payloads
            self._test_payloads(port, normal_response.status_code, results, evidence)
            
            time.sleep(0.5)  # Be polite
        
        return self._compile_results(results, evidence)
    
    def _check_fingerprints(self, response, results, evidence):
        """Check for WAF fingerprints in response"""
        text = (response.text or "").lower()
        headers = {k.lower(): v for k, v in response.headers.items()}
        
        for pattern, vendor, weight, location in FINGERPRINTS:
            pat = re.compile(pattern, re.I)
            
            if location == "header":
                for header_name, header_value in headers.items():
                    if pat.search(header_name) or pat.search(header_value):
                        results[vendor] += weight
                        evidence.append(f"Header match: {header_name}: {header_value}")
                        
            elif location == "body" and pat.search(text):
                results[vendor] += weight
                evidence.append(f"Body match: {pattern}")
                
            elif location == "cookie":
                cookie_str = "; ".join([f"{c.name}={c.value}" for c in response.cookies])
                if pat.search(cookie_str):
                    results[vendor] += weight
                    evidence.append(f"Cookie match: {cookie_str}")
    
    def _test_payloads(self, port, normal_status, results, evidence):
        """Test with malicious payloads to trigger WAF"""
        test_payloads = XSS_PAYLOADS + SQLI_PAYLOADS
        
        for payload in test_payloads[:6]:  # Limit to 6 payloads
            # Test in URL parameter
            url = self._make_url(port, f"/?q={requests.utils.quote(payload)}")
            malicious_response = self._request(url)
            
            if malicious_response and malicious_response.status_code != normal_status:
                if malicious_response.status_code in (403, 406, 429, 444, 499, 999):
                    results["Generic WAF"] += 3
                    evidence.append(f"Blocked payload: {payload} (Status: {malicious_response.status_code})")
            
            time.sleep(0.2)
    
    def _compile_results(self, results, evidence):
        """Compile and return WAF detection results"""
        if not results:
            return []
        
        compiled = []
        max_score = max(results.values()) if results else 0
        
        for vendor, score in results.items():
            confidence = min(100, int((score / max_score) * 100)) if max_score > 0 else 0
            if confidence > 20:  # Only report if confidence > 20%
                compiled.append({
                    "vendor": vendor,
                    "confidence": confidence,
                    "evidence": [e for e in evidence if vendor.lower() in e.lower() or "Generic" in vendor]
                })
        
        return sorted(compiled, key=lambda x: x["confidence"], reverse=True)

class PortScanner:
    def __init__(self, target, max_threads=1000, timeout=1, verbose=False):
        self.target = target
        self.max_threads = max_threads
        self.timeout = timeout
        self.verbose = verbose
        self.open_ports = []
        self.scan_time = 0
        self.web_ports = []
        
        self.resolved_ip = self._resolve_target()
        
    def _resolve_target(self):
        try:
            # Check if it's already an IP address
            try:
                ipaddress.ip_address(self.target)
                return self.target
            except ValueError:
                # It's a domain, resolve it
                ip = socket.gethostbyname(self.target)
                print(f"[{Fore.LIGHTCYAN_EX}*{Style.RESET_ALL}] Resolved {Fore.YELLOW}{self.target}{Style.RESET_ALL} to {Fore.GREEN}{ip}{Style.RESET_ALL}")
                return ip
        except socket.gaierror:
            print(f"[{Fore.RED}!{Style.RESET_ALL}] Could not resolve {self.target}")
            return None
    
    def scan_port(self, port):
        """Scan a single port"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.resolved_ip, port))
                
                if result == 0:
                    service_name = self._get_service_name(port)
                    self.open_ports.append(port)
                    
                    # Track web ports for WAF detection
                    if port in [80, 443, 8080, 8443]:
                        self.web_ports.append(port)
                    
                    print(f"[{Fore.LIGHTCYAN_EX}*{Style.RESET_ALL}] {Fore.YELLOW}Port {port}{Style.RESET_ALL} ({service_name}) - {Fore.GREEN}OPEN{Style.RESET_ALL}")
                    return port, service_name
                    
        except Exception as e:
            if self.verbose:
                print(f"[{Fore.RED}!{Style.RESET_ALL}] Error scanning port {port}: {e}")
        return None
    
    def _get_service_name(self, port):
        """Get service name for common ports"""
        common_services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
            995: "POP3S", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
            27017: "MongoDB", 6379: "Redis", 8080: "HTTP-ALT", 8443: "HTTPS-ALT"
        }
        return common_services.get(port, "Unknown")
    
    def scan_range(self, start_port=1, end_port=1000):
        """Scan a range of ports"""
        if not self.resolved_ip:
            return []
        
        print(f"[{Fore.LIGHTCYAN_EX}&{Style.RESET_ALL}] Scanning {Fore.YELLOW}{self.target}{Style.RESET_ALL} ({self.resolved_ip})")
        print(f"[{Fore.LIGHTCYAN_EX}&{Style.RESET_ALL}] Port range: {Fore.GREEN}{start_port}-{end_port}{Style.RESET_ALL}")
        print(f"[{Fore.LIGHTCYAN_EX}&{Style.RESET_ALL}] Threads: {Fore.BLUE}{self.max_threads}{Style.RESET_ALL}")
        
        start_time = time.time()
        ports_to_scan = range(start_port, end_port + 1)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            results = executor.map(self.scan_port, ports_to_scan)
            list(results)  # Consume the generator
        
        self.scan_time = time.time() - start_time
        return self.open_ports
    
    def scan_custom_ports(self, ports):
        """Scan custom list of ports"""
        if not self.resolved_ip:
            return []
        
        print(f"[{Fore.LIGHTCYAN_EX}&{Style.RESET_ALL}] Scanning {Fore.YELLOW}{self.target}{Style.RESET_ALL} ({self.resolved_ip})")
        print(f"[{Fore.LIGHTCYAN_EX}&{Style.RESET_ALL}] Ports: {Fore.GREEN}{ports}{Style.RESET_ALL}")
        
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            results = executor.map(self.scan_port, ports)
            list(results)  # Consume the generator
        
        self.scan_time = time.time() - start_time
        return self.open_ports
    
    def scan_common_ports(self):
        """Scan common ports"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 
                       3306, 3389, 5432, 5900, 6379, 27017, 5000, 8000, 8080, 8443]
        return self.scan_custom_ports(common_ports)
    
    def detect_waf(self):
        """Detect WAF if web ports are open"""
        if not self.web_ports:
            print(f"[{Fore.YELLOW}!{Style.RESET_ALL}] No web ports open, skipping WAF detection")
            return []
        
        print(f"\n[{Fore.LIGHTCYAN_EX}WAF{Style.RESET_ALL}] Web ports detected: {self.web_ports}")
        print(f"[{Fore.LIGHTCYAN_EX}WAF{Style.RESET_ALL}] Starting WAF detection...")
        
        # Determine scheme (prioritize HTTPS)
        scheme = "https" if 443 in self.web_ports or 8443 in self.web_ports else "http"
        
        try:
            detector = WAFDetector(self.target, scheme)
            waf_results = detector.detect_waf()
            
            if waf_results:
                print(f"\n[{Fore.GREEN}WAF DETECTED{Style.RESET_ALL}]")
                for result in waf_results:
                    print(f"  {Fore.YELLOW}{result['vendor']}:{Style.RESET_ALL} {result['confidence']}% confidence")
                    for evidence in result['evidence'][:2]:  # Show top 2 evidence
                        print(f"    - {evidence}")
            else:
                print(f"[{Fore.GREEN}*{Style.RESET_ALL}] {Fore.GREEN}No WAF detected{Style.RESET_ALL}")
            
            return waf_results
            
        except Exception as e:
            print(f"[{Fore.RED}!{Style.RESET_ALL}] WAF detection failed: {e}")
            return []
    
    def service_version_detection(self, port):
        """Attempt to detect service version using socket banner grabbing"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(3)
                sock.connect((self.resolved_ip, port))
                
                # Try to receive banner
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                if banner:
                    print(f"[{Fore.GREEN}i{Style.RESET_ALL}] Port {port} Banner: {Fore.CYAN}{banner[:100]}{Style.RESET_ALL}")
                    return banner
        except:
            pass
        return None
    
    def nmap_version_scan(self, ports=None):
        """Use nmap for detailed version detection (if available)"""
        if not ports:
            ports = self.open_ports
        
        if not ports:
            print(f"[{Fore.YELLOW}!{Style.RESET_ALL}] No open ports found for version detection")
            return
        
        try:
            port_str = ','.join(map(str, ports))
            print(f"[{Fore.LIGHTCYAN_EX}&{Style.RESET_ALL}] Running nmap version detection on ports: {port_str}")
            
            result = subprocess.run(
                ['nmap', '-sV', '-p', port_str, self.resolved_ip],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print(f"\n[{Fore.GREEN}NMAP RESULTS{Style.RESET_ALL}]")
                print(result.stdout)
            else:
                print(f"[{Fore.RED}!{Style.RESET_ALL}] Nmap scan failed")
                
        except FileNotFoundError:
            print(f"[{Fore.RED}!{Style.RESET_ALL}] Nmap not found. Please install nmap for detailed version detection.")
        except subprocess.TimeoutExpired:
            print(f"[{Fore.RED}!{Style.RESET_ALL}] Nmap scan timed out")

def main():
    parser = argparse.ArgumentParser(description='Advanced Port Scanner with WAF Detection')
    parser.add_argument('target', help='Target IP or domain to scan')
    parser.add_argument('-p', '--ports', help='Ports to scan (e.g., 80,443 or 1-1000)')
    parser.add_argument('-t', '--threads', type=int, default=1000, help='Number of threads (default: 1000)')
    parser.add_argument('-c', '--common', action='store_true', help='Scan common ports only')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--nmap', action='store_true', help='Run nmap version detection on open ports')
    parser.add_argument('--banner', action='store_true', help='Attempt banner grabbing')
    parser.add_argument('--waf', action='store_true', help='Enable WAF detection')
    parser.add_argument('--nowaf', action='store_true', help='Disable WAF detection')
    
    args = parser.parse_args()
    
    # Create scanner
    scanner = PortScanner(args.target, max_threads=args.threads, verbose=args.verbose)
    
    # Determine ports to scan
    ports = None
    if args.ports:
        if '-' in args.ports:
            start, end = map(int, args.ports.split('-'))
            ports = list(range(start, end + 1))
        elif ',' in args.ports:
            ports = list(map(int, args.ports.split(',')))
        else:
            ports = [int(args.ports)]
    
    # Perform scan
    if args.common:
        open_ports = scanner.scan_common_ports()
    elif ports:
        open_ports = scanner.scan_custom_ports(ports)
    else:
        open_ports = scanner.scan_range(1, 1000)  # Default range
    
    # Print summary
    print(f"\n[{Fore.LIGHTCYAN_EX}SUMMARY{Style.RESET_ALL}]")
    print(f"Scan completed in {Fore.GREEN}{scanner.scan_time:.2f}{Style.RESET_ALL} seconds")
    print(f"Open ports found: {Fore.GREEN}{len(open_ports)}{Style.RESET_ALL}")
    
    if open_ports:
        print(f"Ports: {Fore.YELLOW}{sorted(open_ports)}{Style.RESET_ALL}")
    
    # Additional scans
    if args.banner and open_ports:
        print(f"\n[{Fore.LIGHTCYAN_EX}BANNER GRABBING{Style.RESET_ALL}]")
        for port in open_ports:
            scanner.service_version_detection(port)
    
    if args.nmap and open_ports:
        scanner.nmap_version_scan()
    
    # WAF detection (auto if web ports found, or explicit)
    if not args.nowaf and (args.waf or scanner.web_ports):
        scanner.detect_waf()

if __name__ == "__main__":
    main()