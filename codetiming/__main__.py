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
    script = sys.argv[args["arg_start_idx"] :]
    name = normalize_name(args["tag"], *script)

    # Run script
    timestamp = datetime.now()
    runtime = run_script(script=script, tag=args["tag"])
    store_run(name=name, timestamp=timestamp, runtime=runtime)

    # Report
    tag, _, script_str = name.partition("_")
    stats = get_stats(script=script_str)
    console.print(show_table(stats=stats, script=script_str, current_tag=tag))
    console.print(show_plot(stats=stats, script=script_str, current_tag=tag))


def run_script(script, tag):
    """Run the script and return the running time"""
    cmd = [sys.executable, *script]
    console.print(
        f"Running [cyan]{pathlib.Path(cmd[0]).name} {' '.join(script)}[/] "
        f"with tag [cyan]{tag}[/]"
    )
    with (timer := Timer(logger=console.print)):
        subprocess.run(cmd)

    return timer.last


def store_run(name, timestamp, runtime):
    """Save information about the run to file"""
    path = STATS_PATH / f"{name}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open(mode="at", encoding="utf-8") as fid:
        fid.write(f"{timestamp.isoformat()},{runtime}\n")


def get_stats(script):
    """Get statistics for all runs of this script"""
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

    return stats


def show_table(stats, script, current_tag):
    """Show statistics in a table"""
    tags = sorted(stats.keys(), key=lambda tag: mean(stats[tag]["times"]))

    # Set up a Rich table
    table = Table(title=f"Codetiming: {script}")
    table.add_column("Tag", justify="right", width=30, style="green", no_wrap=True)
    table.add_column("Last", justify="right", width=8)
    table.add_column("#", justify="right", width=4)
    table.add_column("Min", justify="right", width=8)
    table.add_column("Mean", justify="right", width=8)
    table.add_column("Max", justify="right", width=8)
    table.add_column(f"vs {current_tag}", justify="right", width=12)
    ref_mean = mean(stats[current_tag]["times"])

    # Fill in data
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
    return table


def show_plot(stats, script, current_tag):
    """Show statistics over time in a plot"""
    data = stats[current_tag]
    if len(data["times"]) < 2:
        return

    return (
        f"\nCodetimings of [bold cyan]{script} ({current_tag})[/] over time\n"
        + plotille.plot(data["timestamps"], data["times"], height=20, width=80)
    )


def parse_args(args):
    """Parse codetiming arguments while ignoring those for the script

    We can't use argparse or similar tools because they will raise issues with
    the script arguments.
    """
    options = {"-t": ("tag", str), "--tag": ("tag", str)}
    option_values = {"tag": "default"}
    arg_start_idx = 1

    if len(args) <= arg_start_idx:
        show_help()

    while args[arg_start_idx] in options:
        option, parser = options[args[arg_start_idx]]
        if len(args) <= arg_start_idx + 2:
            show_help()
        option_values[option] = parser(args[arg_start_idx + 1])
        arg_start_idx += 2

    return dict(option_values, arg_start_idx=arg_start_idx)


def show_help():
    """Show help and quit"""
    print(__doc__)
    raise SystemExit(1)


def normalize_name(*name_parts):
    """Create a normalized name for the script that has been run"""
    return "_".join(re.sub(r"[^\w-]", "-", part) for part in name_parts)


if __name__ == "__main__":
    main()
