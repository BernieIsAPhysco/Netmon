#!/usr/bin/env python3
from monitor.connections import build_snapshot, enrich_connections
from monitor.ui import render_table
from monitor.export import export_csv, export_pretty
from rich.live import Live
from rich.console import Console
import time

REFRESH_INTERVAL = 2.0  # seconds

console = Console()


def main_loop():
    console.print("[bold green]Starting NetMon — press CTRL+C to quit.[/]")
    with Live(refresh_per_second=4, console=console) as live:
        try:
            while True:
                conns = build_snapshot()
                conns = enrich_connections(conns)
                panel = render_table(conns)
                live.update(panel)
                time.sleep(REFRESH_INTERVAL)
        except KeyboardInterrupt:
            console.print("\n[bold]Interrupted by user.[/]")
            ans = input("Export snapshot? (1=CSV, 2=Pretty Table, Enter=skip): ").strip()
            if ans == "1":
                fname = export_csv(conns)
                console.print(f"Saved CSV snapshot -> {fname}")
            elif ans == "2":
                fname = export_pretty(conns)
                console.print(f"Saved Pretty Table snapshot -> {fname}")
            else:
                console.print("No export selected.")
            console.print("Bye.")


if __name__ == "__main__":
    main_loop()
