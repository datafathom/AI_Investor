import subprocess
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def sanitize_jsx_files(directory_path: str):
    """Recursively removes non-ASCII characters from all .jsx files."""
    path = Path(directory_path)
    for file in path.rglob("*.jsx"):
        try:
            with open(file, 'rb') as f:
                content = f.read()
            
            # Filter out bytes > 127
            sanitized = bytes([b for b in content if b <= 127])
            
            if content != sanitized:
                logger.info(f"Sanitized: {file.relative_to(path.parent.parent)}")
                with open(file, 'wb') as f:
                    f.write(sanitized)
        except Exception as e:
            logger.error(f"Failed to sanitize {file}: {e}")

def run_clean_build(**kwargs):
    """
    Sanitizes all JSX files and then runs the frontend build.
    """
    cwd = os.getcwd()
    frontend_src = os.path.join(cwd, "frontend2", "src")
    
    logger.info("Starting clean build (Sanitization + Build)...")
    print("Sanitizing JSX files (ASCII only)...")
    sanitize_jsx_files(frontend_src)
    
    return run_frontend_build(**kwargs)


def run_frontend_build(**kwargs):
    """
    Executes the frontend build process.
    """
    cwd = os.getcwd()
    frontend_path = os.path.join(cwd, "frontend2")
    
    logger.info("Starting frontend build...")
    print(f"Building frontend in {frontend_path}...")
    
    try:
        # Run npm run build
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=frontend_path,
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("Frontend build successful.")
            print(result.stdout)
            return True
        else:
            logger.error(f"Frontend build failed with exit code {result.returncode}")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        logger.exception("An error occurred during frontend build.")
        print(f"Error: {str(e)}")
        return False
