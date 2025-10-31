import argparse
import asyncio
import ipaddress
import os
import socket
import struct
import time
from typing import List
from colorama import init, Fore, Style

init()

FIXED_CONCURRENCY = 20
FIXED_RATE = 50.0

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0

def checksum(source: bytes) -> int:
    data = source if len(source) % 2 == 0 else source + b"\x00"
    
    s = 0
    for i in range(0, len(data), 2):
        w = (data[i] << 8) | data[i + 1]
        s += w
    s = (s >> 16) + (s & 0xFFFF)
    s += s >> 16
    return (~s) & 0xFFFF

def make_packet(id: int, seq: int, payload: bytes = b"abcdefghijklmnopqrstuvwabcdefghi") -> bytes:
    header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, 0, id, seq)
    chk = checksum(header + payload)
    header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, chk, id, seq)
    return header + payload

def _sync_ping(dest_ip: str, timeout: float, id: int, seq: int) -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.settimeout(timeout)

        packet = make_packet(id, seq)
        send_time = time.time()
        sock.sendto(packet, (dest_ip, 0))
        
        while True:
            try:
                rec_packet, addr = sock.recvfrom(1024)
                ip_header_len = (rec_packet[0] & 0x0F) * 4
                icmp_header = rec_packet[ip_header_len:ip_header_len + 8]
                if len(icmp_header) < 8:
                    continue
                r_type, r_code, r_chksum, r_id, r_seq = struct.unpack("!BBHHH", icmp_header)
                if r_type == ICMP_ECHO_REPLY and r_id == id and r_seq == seq:
                    sock.close()
                    return True
            except socket.timeout:
                break
            if time.time() - send_time > timeout:
                break
    except socket.timeout:
        return False
    except PermissionError:
        raise
    except Exception:
        return False
    finally:
        try:
            sock.close()
        except Exception:
            pass
    return False

async def ping(dest_ip: str, timeout: float, executor, id: int, seq: int) -> bool:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _sync_ping, dest_ip, timeout, id, seq)

async def run_sweep(
    network_prefix: str,
    start: int,
    end: int,
    timeout: float,
):
    print(f"{Fore.YELLOW}[!] Starting ping sweep. Press Ctrl+C to cancel at any time.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Target: {network_prefix}.{start}-{end}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Timeout: {timeout}s, Concurrency: {FIXED_CONCURRENCY}, Rate: {FIXED_RATE}/s{Style.RESET_ALL}")
    print()
    
    try:
        if "/" in network_prefix:
            net = ipaddress.ip_network(network_prefix, strict=False)
            base = str(net.network_address)
            prefix_octets = base.split(".")[:3]
            prefix = ".".join(prefix_octets)
        else:
            octs = network_prefix.split(".")
            if len(octs) == 4:
                prefix = ".".join(octs[:3])
            elif len(octs) == 3:
                prefix = network_prefix
            else:
                raise ValueError("Invalid network prefix")
    except Exception as e:
        raise ValueError(f"Invalid network prefix: {e}")
    
    sem = asyncio.Semaphore(FIXED_CONCURRENCY)
    results: list[str] = []
    
    import concurrent.futures
    
    max_workers = max(4, FIXED_CONCURRENCY)
    delay_between = 0 if FIXED_RATE <= 0 else 1.0 / FIXED_RATE
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        tasks = []
        seq_num = 0
        pid = os.getpid() & 0xFFFF
        
        async def sem_ping(ip: str, seqnum: int):
            async with sem:
                if delay_between > 0:
                    await asyncio.sleep(delay_between)
                try:
                    got = await ping(ip, timeout, pool, pid, seqnum)
                    return ip, got
                except PermissionError:
                    raise
                except Exception:
                    return ip, False
            
        total = end - start + 1
        printed = 0
        start_time = time.time()
        
        for i in range(start, end + 1):
            addr = f"{prefix}.{i}"
            seq_num += 1
            task = asyncio.create_task(sem_ping(addr, seq_num))
            tasks.append(task)
        
        for future in asyncio.as_completed(tasks):
            try:
                ip, alive = await future
            except PermissionError:
                print(f"{Fore.RED}[!] Error: you must run this program as root/administrator to send ICMP packets (raw sockets). Exiting.{Style.RESET_ALL}")
                return
            except Exception:
                continue
            
            printed += 1
            if alive:
                print(f"{Fore.GREEN}[+] {ip} is alive{Style.RESET_ALL}")
                results.append(ip)
            else:
                print(f"{Fore.RED}[-] {ip} is dead{Style.RESET_ALL}")
            
            if printed % 10 == 0 or printed == total:
                elapsed = time.time() - start_time
                rate_done = printed / elapsed if elapsed > 0 else 0
                remaining = total - printed
                eta = remaining / rate_done if rate_done > 0 else 0
                print(f"{Fore.YELLOW}[*] Progress: {printed}/{total} ({printed/total*100:.1f}%), Rate: {rate_done:.1f} req/s, ETA: {eta:.1f}s{Style.RESET_ALL}")
                
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Ping sweep complete!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Total alive hosts: {len(results)}{Style.RESET_ALL}")
    
    if results:
        print(f"\n{Fore.GREEN}[+] Alive hosts:{Style.RESET_ALL}")
        for host in sorted(results, key=lambda ip: [int(octet) for octet in ip.split('.')]):
            print(f"  {Fore.GREEN}- {host}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}[!] No alive hosts found{Style.RESET_ALL}")
    print("")
    print("The rest is Dead...      :(")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")

def parse_args():
    p = argparse.ArgumentParser(description="ICMP / Ping sweep")
    p.add_argument("prefix", help="IP prefix (e.g. 192.168.1 or 192.168.1.0/24)")
    p.add_argument("--start", type=int, default=1, help="start host (default 1)")
    p.add_argument("--end", type=int, default=254, help="end host (default 254)")
    p.add_argument("-t", "--timeout", type=float, default=1.0, help="per-ping timeout in seconds (default 1.0)")
    p.add_argument("-c", "--concurrency", type=int, default=20, help="max concurrent pings (default 20)")
    p.add_argument("-r", "--rate", type=float, default=50.0, help="max pings per second (default 50)")
    return p.parse_args()

def main():
    args = parse_args()
    if args.start < 0 or args.start > 254 or args.end < 0 or args.end > 254 or args.start > args.end:
        raise SystemExit(f"{Fore.RED}[!] Invalid start/end range (must be between 0-254 and start <= end){Style.RESET_ALL}")
    
    global FIXED_CONCURRENCY, FIXED_RATE
    FIXED_CONCURRENCY = args.concurrency
    FIXED_RATE = args.rate
    
    try:
        asyncio.run(run_sweep(args.prefix, args.start, args.end, args.timeout))
    except ValueError as ve:
        print(f"{Fore.RED}[!] Error: {ve}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Interrupted by user.{Style.RESET_ALL}")
    except PermissionError:
        print(f"{Fore.RED}[!] Error: you must run this program as root/administrator to send ICMP packets (raw sockets).{Style.RESET_ALL}")
        
if __name__ == "__main__":
    main()