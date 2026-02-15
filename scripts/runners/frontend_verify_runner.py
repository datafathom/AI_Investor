"""
===============================================================================
FILE: scripts/runners/frontend_verify_runner.py
ROLE: CLI Runner for Frontend Verification
PURPOSE: Handles URL extraction from files and triggers robust verification.
===============================================================================
"""

import os
import re
import sys
import logging
from pathlib import Path
import datetime
import json
import subprocess
from typing import List, Dict, Any

# Setup path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import the batch logic
from scripts.verify_routes_batch import run_batch_verification
from scripts.util.base_verifier import BaseVerifier

logger = logging.getLogger(__name__)

def extract_urls_from_file(file_path: Path) -> List[str]:
    """
    Extracts URLs from a file (.md, .py, .txt).
    Handles markdown lists, python arrays, and raw text.
    """
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return []

    urls = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Pattern for http(s)://
            url_pattern = r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            matches = re.findall(url_pattern, content)
            
            # Clean matches (remove trailing quotes or brackets from python/markdown)
            for m in matches:
                clean_url = m.strip('"\',()[]')
                if clean_url not in urls:
                    urls.append(clean_url)
                    
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        
    return urls

def verify_urls(file_path: str, **kwargs):
    """
    Handler for: python cli.py frontend verify urls <path>
    """
    abs_path = PROJECT_ROOT / file_path
    urls = extract_urls_from_file(abs_path)
    
    if not urls:
        print(f"No URLs found in {file_path}")
        return

    print(f"Found {len(urls)} URLs to verify.")
    
    # We need to convert full URLs (http://localhost:5173/...) to relative routes (/...)
    # for the run_batch_verification logic which prepends base_url.
    # Actually, we can just pass them as is if we modify the batch runner slightly, 
    # but let's keep it consistent.
    
    routes = []
    for u in urls:
        if "localhost:5173" in u:
            routes.append(u.split("localhost:5173")[-1])
        elif "127.0.0.1:5173" in u:
            routes.append(u.split("127.0.0.1:5173")[-1])
        else:
            # Assume it's a relative route already if it starts with /
            if u.startswith("/"):
                routes.append(u)
            else:
                logger.warning(f"Skipping unknown URL format: {u}")

    # Extract department name from filename (e.g. 'architect_routes.py' -> 'architect')
    dept_name = None
    filename = os.path.basename(file_path)
    if "_routes.py" in filename:
        dept_name = filename.replace("_routes.py", "")
    elif "routes.py" in filename: # Fallback if just routes.py
        dept_name = filename.replace("routes.py", "").strip("_")
    
    if dept_name:
        print(f"Detected Department: {dept_name}")

    if not routes:
        print("No valid local routes extracted.")
        return

    run_batch_verification(routes, max_retries=kwargs.get("retries", 8), dept_name=dept_name)
    send_audit_summary_to_slack(dept_name=dept_name)

def send_audit_summary_to_slack(dept_name: str = None):
    """
    Reads the latest results JSON and sends a formatted summary to Slack.
    """
    today_str = datetime.datetime.now().strftime("%m_%d_%y")
    results_dir = PROJECT_ROOT / "DEBUGGING" / "FrontEndAudit" / "results"
    
    if dept_name:
        results_file = results_dir / f"{dept_name}_results" / f"{dept_name}_{today_str}_verify_results.json"
    else:
        results_file = results_dir / f"{today_str}_verify_results.json"
    
    if not results_file.exists():
        print(f"No results found for {today_str} to send to Slack.")
        return

    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to read results JSON: {e}")
        return

    if not data:
        return

    failed_routes = [d['route'] for d in data if d['status'] != 'SUCCESS']
    success_routes = [d['route'] for d in data if d['status'] == 'SUCCESS']

    message = "<<==#### FRONTEND ROUTES AUDIT ####==>>\n"
    if failed_routes:
        message += "## FAILED ROUTES\n"
        for r in failed_routes:
            message += f"* {r} - fail\n"
        message += "\n"
    
    if success_routes:
        message += "## SUCCESSFUL ROUTES \n"
        for r in success_routes:
            message += f"* {r} - success \n"

    # Use CLI to send to Slack (handling venv if possible, but direct call is safer here)
    cmd = [sys.executable, str(PROJECT_ROOT / "cli.py"), "slack", "send", message]
    if failed_routes:
        cmd.extend(["--level", "warning"])
    else:
        cmd.extend(["--level", "success"])
        
    print(f"Sending audit summary to Slack ({len(failed_routes)} failed, {len(success_routes)} success)...")
    subprocess.run(cmd, capture_output=True)

def verify_single_url(url: str, **kwargs):
    """
    Handler for: python cli.py frontend verify url <url>
    """
    # Convert to relative route
    route = url
    if "localhost:5173" in url:
        route = url.split("localhost:5173")[-1]
    elif "127.0.0.1:5173" in url:
        route = url.split("127.0.0.1:5173")[-1]

    print(f"Verifying individual route: {route}")
    
    # Use run_batch_verification for consistency (supports retries)
    run_batch_verification([route], max_retries=kwargs.get("retries", 8))
    send_audit_summary_to_slack()

def verify_by_dept(dept: str, **kwargs):
    """
    Handler for: python cli.py frontend verify --dept <name>
    """
    # Construct the path to the dept routes file
    # Pattern seems to be: DEBUGGING/FrontEndAudit/Routes2Test/depts/{dept}_routes.py
    
    filename = f"{dept}_routes.py"
    file_path = PROJECT_ROOT / "DEBUGGING" / "FrontEndAudit" / "Routes2Test" / "depts" / filename
    
    if not file_path.exists():
        logger.error(f"Routes file not found for department '{dept}' at {file_path}")
        print(f"Error: Could not find routes file: {file_path}")
        return

    print(f"Targeting department: {dept} -> {file_path}")
    # Normalize path to string relative to project root if possible, or absolute
    rel_path = file_path.relative_to(PROJECT_ROOT)
    verify_urls(str(rel_path), **kwargs)
