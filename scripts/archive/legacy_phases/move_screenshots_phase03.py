
import os
import shutil
import glob

# Source: Artifact Directory
source_dir = r"C:/Users/astir/.gemini/antigravity/brain/4ae89fc2-176a-4a43-9e82-57075f798ef9/"

# Destination: Project Screenshots Directory
dest_dir = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\screenshots"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# Pattern to match the Phase 03 screenshots
patterns = [
    "Phase03_*.png"
]

count = 0
for pattern in patterns:
    search_path = os.path.join(source_dir, pattern)
    files = glob.glob(search_path)
    
    for file_path in files:
        try:
            filename = os.path.basename(file_path)
            dest_path = os.path.join(dest_dir, filename)
            # Handle duplicates
            if os.path.exists(dest_path):
                 base, extend = os.path.splitext(filename)
                 dest_path = os.path.join(dest_dir, f"{base}_copy{extend}")
                 
            shutil.copy2(file_path, dest_path)
            # os.remove(file_path) # Optional, keeping for now or can delete
            print(f"Moved: {filename}")
            count += 1
        except Exception as e:
            print(f"Error moving {file_path}: {e}")

print(f"Successfully moved {count} screenshots.")
