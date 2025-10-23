#!/usr/bin/env python3
# encoding: utf-8
r"""

Chrome Tab Manager

CLI tool to list and close Chrome browser tabs from the command line on macOS.

## Overview

Uses AppleScript via osascript to interact with Chrome tabs.

## Installation

### Prerequisites

- macOS (requires AppleScript support)
- Python 3.7 or higher
- Google Chrome browser

### Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

Or install packages individually:

```bash
python3 -m pip install rich typer doc2md
```

### Make Executable (Optional)

```bash
chmod +x chrometabs.py
```

### macOS Permissions

On macOS, you need to grant Terminal (or your terminal app) permission to control Chrome:

1. Run the script once - it will fail but trigger the permission request
2. Go to System Settings/Preferences > Privacy & Security > Automation
3. Enable Terminal (or your terminal app) to control Google Chrome

Alternatively, test AppleScript access directly:

```bash
osascript -e 'tell application "Google Chrome" to get URL of active tab of front window'
```

If this returns an error about permissions, follow the steps above.

## Commands

- list: Display all open Chrome tabs
- close: Close specific tab(s) by window and tab number

"""

#
# Imports
#
from typing import List
from rich import print
from rich import traceback
from rich import pretty
from rich.console import Console
from rich.table import Table
import typer
import subprocess
import json

pretty.install()
traceback.install()
console = Console()

app = typer.Typer(
    add_completion=False,
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="Chrome Tab Manager",
    epilog="To get help about the script, call it with the --help option."
)

#
# Helper Functions
#
def get_chrome_tabs():
    """Get all Chrome tabs with window and tab indices."""
    script = '''
    tell application "Google Chrome"
        set output to ""
        repeat with w from 1 to count windows
            repeat with t from 1 to count tabs of window w
                set tabUrl to URL of tab t of window w
                set tabTitle to title of tab t of window w
                set output to output & w & "|" & t & "|" & tabUrl & "|" & tabTitle & linefeed
            end repeat
        end repeat
        return output
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.stdout.strip()

def close_chrome_tab(window, tab):
    """Close a specific Chrome tab."""
    script = f'tell application "Google Chrome" to close tab {tab} of window {window}'
    subprocess.run(['osascript', '-e', script])

#
# Command: List
#
@app.command()
def list():
    """List all open Chrome tabs."""
    tabs_data = get_chrome_tabs()
    
    if not tabs_data:
        console.print("[red]No Chrome tabs found or Chrome not running[/red]")
        return
    
    table = Table(title="Chrome Tabs")
    table.add_column("Window", style="cyan", no_wrap=True)
    table.add_column("Tab", style="magenta", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("URL", style="blue")
    
    for line in tabs_data.split('\n'):
        if line:
            parts = line.split('|')
            if len(parts) == 4:
                window, tab, url, title = parts
                table.add_row(window, tab, title[:50], url[:80])
    
    console.print(table)

#
# Command: Close
#
@app.command()
def close(
    window: int = typer.Argument(..., help="Window number"),
    tabs: List[int] = typer.Argument(..., help="Tab number(s) to close"),
    all: bool = typer.Option(False, "--all", help="Close all tabs in the window")
):
    """Close specific Chrome tab(s)."""
    if all:
        script = f'tell application "Google Chrome" to close every tab of window {window}'
        subprocess.run(['osascript', '-e', script])
        console.print(f"[green]Closed all tabs in window {window}[/green]")
    else:
        # Sort tabs in descending order to avoid index shifting when closing
        for tab in sorted(tabs, reverse=True):
            close_chrome_tab(window, tab)
            console.print(f"[green]Closed tab {tab} in window {window}[/green]")

#
# Command: Doc
#
@app.command()
def doc(
    ctx: typer.Context,
    title: str = typer.Option(None, help="The title of the document"),
    toc: bool = typer.Option(False, help="Whether to create a table of contents"),
) -> None:
    """Re-create the documentation and write it to the output file."""
    import importlib
    import importlib.util
    import sys
    import os
    import doc2md

    def import_path(path):
        module_name = os.path.basename(path).replace("-", "_")
        spec = importlib.util.spec_from_loader(
            module_name,
            importlib.machinery.SourceFileLoader(module_name, path),
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module
        return module

    mod_name = os.path.basename(__file__)
    if mod_name.endswith(".py"):
        mod_name = mod_name.rsplit(".py", 1)[0]
    atitle = title or mod_name.replace("_", "-")
    module = import_path(__file__)
    docstr = module.__doc__
    result = doc2md.doc2md(docstr, atitle, toc=toc, min_level=0)
    print(result)

#
# Main function
#
if __name__ == "__main__":
    try:
        app()
    except SystemExit as e:
        if e.code != 0:
            raise
