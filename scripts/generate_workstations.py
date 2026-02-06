import os
import json
import re

# Paths
BASE_DIR = r"c:\Users\astir\Desktop\AI_Company\AI_Investor"
REGISTRY_PATH = os.path.join(BASE_DIR, "frontend", "src", "config", "departmentRegistry.js")
PAGES_DIR = os.path.join(BASE_DIR, "frontend", "src", "pages", "workstations")
APP_JSX_PATH = os.path.join(BASE_DIR, "frontend", "src", "App.jsx")

TEMPLATE = """import React from 'react';
import '../Workstation.css';

const {name} = () => {{
    return (
        <div className="workstation-container">
            <header className="workstation-header">
                <div className="status-dot pulse"></div>
                <h1>{label} <span className="text-slate-500">//</span> WORKSTATION</h1>
                <div className="flex-1"></div>
                <div className="security-badge">SECURE_CHANNEL_v1.2</div>
            </header>

            <div className="workstation-grid">
                <div className="workstation-main bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                    <h2 className="text-cyan-400 font-mono text-xs uppercase tracking-widest mb-4">Functional Module: {label}</h2>
                    <p className="text-slate-400 font-mono text-sm leading-relaxed mb-6">
                        {description}
                    </p>
                    
                    <div className="terminal-box bg-black/80 rounded border border-slate-700 p-4 font-mono text-[10px] text-cyan-500/80">
                        <div className="mb-1">> INITIALIZING {name}...</div>
                        <div className="mb-1">> SYNCING NEURAL MESH...</div>
                        <div className="mb-1">> ESTABLISHING HANDSHAKE WITH AGENTIC LAYER...</div>
                        <div className="text-green-500">> READY.</div>
                    </div>
                </div>

                <div className="workstation-sidebar flex flex-col gap-4">
                    <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
                        <h3 className="text-slate-500 font-mono text-[10px] uppercase mb-2">Metrics</h3>
                        <div className="metric-row border-b border-slate-800/50 py-2">
                            <span className="text-slate-400 text-xs">Latency:</span>
                            <span className="text-cyan-400 text-xs float-right">12ms</span>
                        </div>
                        <div className="metric-row py-2">
                            <span className="text-slate-400 text-xs">Uptime:</span>
                            <span className="text-cyan-400 text-xs float-right">99.9%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}};

export default {name};
"""

def slug_to_component_name(path):
    # e.g. /strategist/builder -> StrategistBuilder
    parts = [p for p in path.split('/') if p]
    return "".join(p.capitalize().replace('-', '') for p in parts)

def extract_submodules():
    with open(REGISTRY_PATH, 'r') as f:
        content = f.read()
    
    # Simple regex to find subModules. Note: This is fragile but works for current file structure
    # subModules: [ { path: "...", label: "...", description: "..." }, ... ]
    submodule_blocks = re.findall(r'subModules:\s*\[\s*(.*?)\s*\]', content, re.DOTALL)
    
    unique_modules = {}
    for block in submodule_blocks:
        items = re.findall(r'\{\s*path:\s*"(.*?)",\s*label:\s*"(.*?)",\s*description:\s*"(.*?)"\s*\}', block)
        for path, label, description in items:
            if path.startswith('/special/'): continue # Skip special routes
            unique_modules[path] = {'label': label, 'description': description}
    
    return unique_modules

def generate_files(modules):
    if not os.path.exists(PAGES_DIR):
        os.makedirs(PAGES_DIR)
        
    for path, data in modules.items():
        comp_name = slug_to_component_name(path)
        # category is the first part of path
        category = path.split('/')[1]
        category_dir = os.path.join(PAGES_DIR, category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
            
        file_path = os.path.join(category_dir, f"{comp_name}.jsx")
        # Overwrite all to apply CSS fixes
        with open(file_path, 'w') as f:
            f.write(TEMPLATE.format(name=comp_name, label=data['label'], description=data['description']))
        print(f"Generated {file_path}")

if __name__ == "__main__":
    modules = extract_submodules()
    generate_files(modules)
    print(f"Total modules processed: {len(modules)}")
