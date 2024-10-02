# for desktop application
# run command in terminal:
# pyinstaller --clean --onefile update.py

# code by ChatGPT 3.5, o1-preview, 4o

import subprocess
import sys
from datetime import datetime
import platform
import os
import json


def main():
    # Get machine name
    machine_name = platform.node()
    log_dir = os.path.join('update logs', machine_name)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Get timestamp
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Log file path
    log_file = os.path.join(log_dir, f"updated_packages_{timestamp}.txt")

    print(f"Log file path: {log_file}")
    print(f"Checking pip and outdated packages on {machine_name}...")

    # Update pip
    print("Checking pip version...")
    pip_upgrade = False
    try:
        current_pip = subprocess.check_output(
            [sys.executable, '-m', 'pip', '--version'], timeout=60
        ).decode('utf-8').split()[1]

        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
            check=True,
            timeout=300
        )

        latest_pip = subprocess.check_output(
            [sys.executable, '-m', 'pip', '--version'], timeout=60
        ).decode('utf-8').split()[1]

        if current_pip != latest_pip:
            pip_upgrade = True
            current_pip = latest_pip

    except subprocess.CalledProcessError as e:
        print(f"Error checking/updating pip: {e}")
        current_pip = "unknown"

    except subprocess.TimeoutExpired:
        print("Checking pip version took too long!")
        return

    # Check for outdated packages
    print("Pip check complete. Checking for outdated packages...")
    try:
        # Use JSON output for easier parsing
        outdated_packages_output = subprocess.check_output(
            [sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json'], timeout=300
        ).decode('utf-8')

        outdated_packages = json.loads(outdated_packages_output)

    except subprocess.CalledProcessError as e:
        print(f"Error checking outdated packages: {e}")
        outdated_packages = []

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output: {e}")
        outdated_packages = []

    except subprocess.TimeoutExpired:
        print("Checking for outdated packages took too long!")
        return

    with open(log_file, 'w') as file:
        file.write(f"Package update log for {machine_name} on {timestamp}\n")
        file.write("=" * 60 + "\n\n")

        if pip_upgrade:
            file.write(f"Updated pip to version {current_pip}\n\n")
            print(f"Updated pip to version {current_pip}")
        else:
            file.write("pip is already up to date.\n\n")
            print("pip is already up to date.")

        if outdated_packages:
            file.write(f"{len(outdated_packages)} package(s) to update:\n\n")
            print(f"Found {len(outdated_packages)} outdated package(s).")
            print("Outdated packages check complete. Proceeding to update...")

            for package in outdated_packages:
                package_name = package['name']
                current_version = package['version']
                latest_version = package['latest_version']
                try:
                    print(f"Updating {package_name} from {
                          current_version} to {latest_version}...")
                    subprocess.run(
                        [sys.executable, '-m', 'pip', 'install',
                            '--upgrade', package_name],
                        check=True
                    )
                    file.write(f"Updated {package_name} from {
                               current_version} to {latest_version}\n")
                except subprocess.CalledProcessError as e:
                    print(f"Error updating {package_name}: {e}")
                    file.write(f"Error updating {package_name}: {e}\n")
            file.write(f"\nAll packages on {
                       machine_name} are now up to date as of {timestamp}.\n")
        else:
            file.write("All packages are up to date.\n")
            print("All packages are up to date.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Process interrupted by user.")
        sys.exit(1)
