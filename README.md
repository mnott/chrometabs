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
