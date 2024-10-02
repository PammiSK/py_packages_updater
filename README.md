# Update Python Packages

This is a simple desktop application script that checks for outdated Python packages on your system, logs the updates, and optionally updates the packages if any are found.

## Features

- Automatically checks for and updates `pip` to the latest version.
- Lists all outdated Python packages.
- Optionally updates all outdated packages.
- Creates a log file that records the update process.

## How It Works

- The script retrieves the current machine name and creates a folder called `update logs`, where logs are stored.
- It checks if `pip` is up-to-date, and if not, upgrades it.
- It retrieves a list of outdated Python packages using `pip` and logs the information.
- Outdated packages are updated to their latest versions, and this process is also logged.

## Requirements

- Python 3.x
- `pip` package manager (comes with Python installation)

## Installation

### 1. Clone or Download the Project

You can download this project and run the script on your system.

### 2. Generate the Executable (Optional)

If you want to create a standalone executable file for this script, you can use **PyInstaller** to bundle it:

```bash
pip install pyinstaller
pyinstaller --clean --onefile update.py
```

This will generate an executable file (`update.exe`), which can be run without needing to invoke Python explicitly.

## Running the Script

### 1. Running as a Python Script

To run the script as a Python script:

```bash
python update.py
```

### 2. Running the Executable (Optional)

After generating the executable file using **PyInstaller**, you can simply double-click `update.exe` or run it from the command line:

```bash
./update.exe
```

### 3. Output

Once the script runs, it will generate a log file in the `update logs/<machine_name>` directory. The log will contain details of the pip version and any package updates that were performed.

## License

This project is **NOT** for commercialization and is intended for **personal use only**.
