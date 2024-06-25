# for desktop application
# run command in terminal:
# pyinstaller --onefile update.py

# code by Chat GPT 3.5

import subprocess
from datetime import datetime
import platform
import os

# machine name
machine_name = platform.node()
if not os.path.exists(machine_name):
    os.makedirs(machine_name)

# timestamp
now = datetime.now()
timestamp = now.strftime("%d-%m-%y  %H_%M_%S")

# parse package info
def parse_package_info(line):
    parts = line.strip().split()
    return parts[0],parts[2] # package name, latest version

# check for pip update
pip_upgrade = False
try:
    current_pip = subprocess.check_output(['pip', '--version']).decode('utf-8').split()[1]
    subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
    latest_pip = subprocess.check_output(['pip', '--version']).decode('utf-8').split()[1]

    if current_pip != latest_pip:
        pip_upgrade = True
        current_pip = latest_pip
    
except subprocess.CalledProcessError as e:
    print(f"Error checking/updating pip: {e}")
    current_pip = "unknown"

# check for outdated packages
try:
    outdated_packages_output = subprocess.check_output(['pip', 'list', '--outdated']).decode('utf-8')
    lines = outdated_packages_output.strip().split('\n')[2:]
    
except subprocess.CalledProcessError as e:
    print(f"Error checking outdated packages: {e}")
    lines = []

log_file = f"{machine_name}/updated packages {timestamp}.txt"

with open(log_file, 'w') as file:
    if pip_upgrade:
        file.write(f"pip=={current_pip}\n")

    if lines:
        file.write(f"{machine_name} has {len(lines)} package updates (excluding pip).")
        for line in lines:
            try:
                
                package_name, latest_version = parse_package_info(line)
                subprocess.run(['pip', 'install', '--upgrade', package_name], check=True)
                file.write(f"{package_name}=={latest_version}\n")
                
            except subprocess.CalledProcessError as e:
                print(f"Error updating {package_name}: {e}")
                file.write(f"Error updating {package_name}: {e}\n")
        file.write(f"All packages in {machine_name} are now up to date as of {timestamp}.\n")
    else:
        file.write(f"All packages in {machine_name} are up to date as of {timestamp}.\n")
