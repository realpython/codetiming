"""CodeTiming: Time your scripts

Usage: codetiming [-t tag] script.py [script options]
"""

# Standard library imports
import pathlib
import re
import subprocess
import sys
from datetime import datetime
from statistics import mean

# Third party imports
import platformdirs
import plotille
from rich.console import Console
from rich.table import Table

# Codetiming imports
from codetiming import Timer

# Set-up
console = Console()
STATS_PATH = platformdirs.user_cache_path("codetiming")
PREC = 4


def main():
    """Wrap a Python script inside codetiming"""
    args = parse_args(sys.argv)

    # Run process
    cmd = [sys.executable, *sys.argv[args["arg_start_idx"] :]]
    console.print(
        f"Running [cyan]{pathlib.Path(cmd[0]).name} {' '.join(cmd[1:])}[/] "
        f"with tag [cyan]{args['tag']}[/]"
    )
    with (timer := Timer(logger=None)):
        subprocess.run(cmd)

    # Clean-up
    name = normalize_name(args["tag"], *cmd[1:])
    store_run(name=name, runtime=timer.last)
    show_stats(name=name, process=" ".join(cmd[1:]))


def store_run(name, runtime):
    """Save information about run to file"""
    path = STATS_PATH / f"{name}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open(mode="at", encoding="utf-8") as fid:
        fid.write(f"{datetime.now().isoformat()},{runtime}\n")


def show_stats(name, process):
    """Show statistics for all runs"""
    current_tag, _, script = name.partition("_")

    # Read statistics from files
    stat_paths = STATS_PATH.glob(f"*{script}.txt")
    stats = {}
    for path in stat_paths:
        tag, *_ = path.name.partition("_")
        timers = [
            (datetime.fromisoformat(ts), float(time))
            for ts, time in [
                line.split(",")
                for line in path.read_text(encoding="utf-8").strip().split("\n")
            ]
        ]
        stats[tag] = dict(zip(["timestamps", "times"], zip(*timers)))
    tags = sorted(stats.keys(), key=lambda tag: mean(stats[tag]["times"]))

    # Show statistics in a table
    table = Table(title=f"Codetiming: {process}")
    table.add_column("Tag", justify="right", width=30, style="green", no_wrap=True)
    table.add_column("Last", justify="right", width=8)
    table.add_column("#", justify="right", width=4)
    table.add_column("Min", justify="right", width=8)
    table.add_column("Mean", justify="right", width=8)
    table.add_column("Max", justify="right", width=8)
    table.add_column(f"vs {current_tag}", justify="right", width=12)
    ref_mean = mean(stats[current_tag]["times"])

    for tag in tags:
        times = stats[tag]["times"]
        table.add_row(
            tag,
            f"{times[-1]:.{PREC}f}",
            str(len(times)),
            f"{min(times):.{PREC}f}",
            f"{mean(times):.{PREC}f}",
            f"{max(times):.{PREC}f}",
            f"{mean(times) / ref_mean:.2f}x",
            style="cyan bold" if tag == current_tag else None,
        )
    console.print(table)

    # Show statistics over time in a plot
    data = stats[current_tag]
    if len(data["times"]) >= 2:
        plot = plotille.plot(data["timestamps"], data["times"], height=20, width=80)
        console.print(
            f"\nCodetimings of [bold cyan]{process} ({current_tag})[/] over time"
        )
        console.print(plot)


def parse_args(args):
    """Parse codetiming arguments while ignoring those for the script

    We can't use argparse or similar tools because they will raise issues with
    the script arguments.
    """
    parsed = {"tag": "default", "arg_start_idx": 1}

    if len(args) < 2:
        show_help()

    if args[1] in ("-t", "--tag"):
        if len(args) < 4:
            show_help()
        parsed["tag"] = args[2]
        parsed["arg_start_idx"] += 2

    return parsed


def show_help():
    """Show help and quit"""
    print(__doc__)
    raise SystemExit(1)


def normalize_name(*name_parts):
    """Create a normalized name for the script that has been run"""
    return "_".join(re.sub(r"[^\w-]", "-", part) for part in name_parts)


if __name__ == "__main__":
    main()
