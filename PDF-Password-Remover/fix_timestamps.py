import os
import time
import datetime
import sys
import shutil

# Set a minimum timestamp for January 1, 1980
min_date = datetime.datetime(1980, 1, 1)
min_timestamp = time.mktime(min_date.timetuple())

# Path to the build directory
build_dir = "/home/backup_user/VoidProjects/pdf-unlock/PDF-Password-Remover/build/exe.linux-x86_64-3.12"

# Create a backup of the original libz file with correct timestamp
source_zlib = "/usr/lib/x86_64-linux-gnu/libz.so.1.3.1"
fixed_zlib = "/tmp/libz.so.1.3.1.fixed"

if os.path.exists(source_zlib):
    # Create a copy with fixed timestamp
    print(f"Creating fixed version of {source_zlib}")
    shutil.copy2(source_zlib, fixed_zlib)
    os.utime(fixed_zlib, (min_timestamp, min_timestamp))
else:
    print(f"Source file {source_zlib} not found")
    sys.exit(1)

# Create a custom build directory structure and copy files that cx_Freeze will use
libz_paths = [
    os.path.join(build_dir, "lib/pillow.libs/libz.so.1.3.1"),
    os.path.join(build_dir, "lib/PIL/libz.so.1.3.1")
]

# Create the directories and copy the fixed libz
for filepath in libz_paths:
    directory = os.path.dirname(filepath)
    os.makedirs(directory, exist_ok=True)
    
    if os.path.exists(filepath):
        # If file exists, update its timestamp
        print(f"Updating timestamp for: {filepath}")
        os.utime(filepath, (min_timestamp, min_timestamp))
    else:
        # If file doesn't exist yet, copy the fixed version
        print(f"Copying fixed zlib to: {filepath}")
        shutil.copy2(fixed_zlib, filepath)

print("Done fixing timestamps")