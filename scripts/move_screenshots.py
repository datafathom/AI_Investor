
import os
import shutil
import glob
from pathlib import Path

# Source: Artifact Directory
# Note: In the real execution environment, I need to know the artifact dir. 
# Based on the subagent output it is 'C:/Users/astir/.gemini/antigravity/brain/4ae89fc2-176a-4a43-9e82-57075f798ef9/'
source_dir = r"C:/Users/astir/.gemini/antigravity/brain/4ae89fc2-176a-4a43-9e82-57075f798ef9/"

# Destination: Project Screenshots Directory
dest_dir = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\screenshots"

print(f"Moving screenshots from {source_dir} to {dest_dir}...")

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# Pattern to match the screenshots we just took
# They start with 'phase_' or 'Phase_' (case insensitive usually on windows, but let's be specific)
# Subagent saved them as lowercase usually in filename, e.g. phase_57_backtest_....png
patterns = [
    "phase_57_*.png",
    "phase_58_*.png",
    "phase_59_*.png",
    "phase_60_*.png",
    "phase_61_*.png",
    "phase_62_*.png",
    "phase_63_*.png",
    "phase_64_*.png",
    "phase_65_*.png",
    "phase_66_*.png",
    "phase_67_*.png",
    "phase_68_*.png"
]

count = 0
for pattern in patterns:
    search_path = os.path.join(source_dir, pattern)
    files = glob.glob(search_path)
    
    for file_path in files:
        try:
            filename = os.path.basename(file_path)
            dest_path = os.path.join(dest_dir, filename)
            
            # Copy then remove (safer than move across drives/partitions just in case)
            shutil.copy2(file_path, dest_path)
            # os.remove(file_path) # Optional: verify copying first
            
            print(f"Moved: {filename}")
            count += 1
        except Exception as e:
            print(f"Error moving {file_path}: {e}")

print(f"Successfully moved {count} screenshots.")
