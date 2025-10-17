from rich.table import Table
from rich.panel import Panel

def format_geo(geo):
    if not geo:
        return ""
    if "error" in geo:
        return f"[error:{geo['error']}]"
    parts = []
    if geo.get("city"):
        parts.append(geo["city"])
    if geo.get("country"):
        parts.append(geo["country"])
    isp = geo.get("isp")
    return (", ".join(parts) + (f" ({isp})" if isp else "")).strip()

def render_table(conns, limit=200):
    t = Table(show_header=True, header_style="bold magenta")
    t.add_column("App", style="cyan", no_wrap=True)
    t.add_column("PID", style="green", width=6)
    t.add_column("Proto", width=5)
    t.add_column("Local → Remote", style="white", no_wrap=True)
    t.add_column("Remote Host", style="yellow")
    t.add_column("Location / ISP", style="white")
    t.add_column("Status", style="red", width=12)

    conns_sorted = sorted(conns, key=lambda e: (e.get("r_ip") or "zzz", str(e.get("app"))))
    for e in conns_sorted[:limit]:
        local_remote = f"{e.get('laddr') or '-'} → {e.get('raddr') or '-'}"
        rhost = e.get("r_hostname") or e.get("r_ip") or "-"
        geo_text = format_geo(e.get("geo"))
        t.add_row(str(e.get("app")), str(e.get("pid")), e.get("type"),
                  local_remote, rhost, geo_text, e.get("status") or "-")

    footer = f"Connections: {len(conns_sorted)}"
    return Panel.fit(t, title="NetMon", subtitle=footer)
