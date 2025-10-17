import csv
from datetime import datetime
from monitor.ui import format_geo
from rich.table import Table
from rich.console import Console

def export_csv(conns, filename=None):
    """Export connections to a well-formatted CSV with proper headers."""
    if not filename:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"netmon_snapshot_{ts}.csv"

    headers = [
        "Application",
        "PID",
        "Protocol",
        "Local Address",
        "Remote Address",
        "Remote IP",
        "Remote Hostname",
        "Status",
        "Location / ISP",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for e in conns:
            geo_text = format_geo(e.get("geo") or {})
            writer.writerow([
                e.get("app") or "-",
                e.get("pid") or "-",
                e.get("type") or "-",
                e.get("laddr") or "-",
                e.get("raddr") or "-",
                e.get("r_ip") or "-",
                e.get("r_hostname") or "-",
                e.get("status") or "-",
                geo_text or "-",
            ])

    print(f"[+] CSV saved to: {filename}")
    return filename


def export_pretty(conns, filename=None):
    """Export connections as a neatly aligned text table."""
    console = Console(record=True, width=150)
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Application", style="cyan")
    table.add_column("PID", style="green", width=6)
    table.add_column("Protocol", width=5)
    table.add_column("Local Address", style="white")
    table.add_column("Remote Address", style="white")
    table.add_column("Status", style="red", width=12)
    table.add_column("Location / ISP", style="yellow")

    for e in conns:
        geo_text = format_geo(e.get("geo") or {})
        table.add_row(
            str(e.get("app") or "-"),
            str(e.get("pid") or "-"),
            str(e.get("type") or "-"),
            str(e.get("laddr") or "-"),
            str(e.get("raddr") or "-"),
            str(e.get("status") or "-"),
            geo_text or "-"
        )

    output = console.export_text(styles=True)
    if not filename:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"netmon_pretty_{ts}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"[+] Pretty table saved to: {filename}")
    return filename

