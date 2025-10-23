# chrometabs

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
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install rich typer doc2md
```

### Make Executable (Optional)

```bash
chmod +x chrometabs.py
```

## Commands

- list: Display all open Chrome tabs
- close: Close specific tab(s) by window and tab number
