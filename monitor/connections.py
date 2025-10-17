import psutil
import socket
import threading
from monitor.utils import reverse_dns
from monitor.geo import geo_lookup, geo_cache, geo_cache_lock

def build_snapshot():
    """Build a list of network connection entries."""
    try:
        raw = psutil.net_connections(kind='inet4')
    except Exception:
        raw = psutil.net_connections(kind='inet')

    conns = []
    proc_cache = {}

    for c in raw:
        pid = c.pid
        laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ""
        raddr_ip, raddr = None, ""
        if c.raddr:
            raddr = f"{c.raddr.ip}:{c.raddr.port}"
            raddr_ip = c.raddr.ip

        if raddr_ip and (raddr_ip.startswith("127.") or raddr_ip.startswith("169.254.") or raddr_ip == "::1"):
            continue

        pname = "<unknown>"
        if pid:
            if pid not in proc_cache:
                try:
                    pname = psutil.Process(pid).name()
                except Exception:
                    pname = str(pid)
                proc_cache[pid] = pname
            else:
                pname = proc_cache[pid]

        conns.append({
            "app": pname,
            "pid": pid or "",
            "laddr": laddr,
            "raddr": raddr,
            "r_ip": raddr_ip,
            "status": c.status,
            "type": "TCP" if c.type == socket.SOCK_STREAM else "UDP",
        })
    return conns


def enrich_connections(conns):
    """Add reverse DNS and geolocation to each connection."""
    ips = {e["r_ip"] for e in conns if e["r_ip"]}
    for ip in ips:
        with geo_cache_lock:
            if ip not in geo_cache:
                threading.Thread(target=geo_lookup, args=(ip,), daemon=True).start()

    for e in conns:
        ip = e.get("r_ip")
        if ip:
            e["r_hostname"] = reverse_dns(ip)
            with geo_cache_lock:
                cached = geo_cache.get(ip)
            e["geo"] = cached[1] if cached else {"note": "querying"}
        else:
            e["r_hostname"] = ""
            e["geo"] = {}
    return conns
