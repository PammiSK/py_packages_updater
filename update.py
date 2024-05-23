# for desktop application
# run command in terminal:
# pyinstaller --onefile update.py

# code by Chat GPT 3.5

import subprocess
from datetime import datetime

# Function to parse package information
def parse_package_info(line):
    parts = line.strip().split()
    return parts[0],parts[2]  # Return package name and latest version

# Run pip list --outdated command to check for outdated packages
outdated_packages_output = subprocess.check_output(['pip', 'list', '--outdated']).decode('utf-8')

# Split the output into lines and skip the first line (header)
lines = outdated_packages_output.strip().split('\n')[2:]

# Get the current date and time
now = datetime.now()
# Format the date and time as DDMMYYHHmmSS
timestamp = now.strftime('%d%m%y%H%M%S')

# Iterate over each line, parse package info, and update the package
with open(f"updated_packages_{timestamp}.txt", 'w') as file:
    if lines:
        for line in lines:
            package_name, latest_version = parse_package_info(line)
            file.write(f"{package_name}=={latest_version}\n")
            subprocess.run(['pip', 'install', '--upgrade', package_name])
    else:
        file.write("All packages are up to date")

print("All packages updated successfully!")
