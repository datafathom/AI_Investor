import os
import http.server
import socketserver
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Sovereign OS Internal Documentation Server")

# Allow CORS for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DOCS_ROOT = Path(__file__).parent.parent / "docs"
VIEWER_DIST = DOCS_ROOT / "viewer" / "dist"

def get_file_tree(path: Path):
    tree = []
    if not path.exists(): return tree
    
    items = list(path.iterdir())
    # Sort: directories first, then alphabetical
    items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

    for item in items:
        # Ignore hidden files, node_modules, and viewer app folders
        if item.name.startswith('.') or item.name in ['node_modules', 'viewer', 'dist', '__pycache__']:
            continue
            
        relative_path = item.relative_to(DOCS_ROOT).as_posix()
        if item.is_dir():
            # Only include directories that have .md or .txt files inside them (recursively)
            children = get_file_tree(item)
            has_docs = any(f.suffix in ['.md', '.txt'] for f in item.glob('**/*') if f.is_file())
            if children or has_docs:
                tree.append({
                    "name": item.name,
                    "type": "directory",
                    "path": relative_path,
                    "children": children
                })
        elif item.suffix in ['.md', '.txt']:
            tree.append({
                "name": item.name,
                "type": "file",
                "path": relative_path
            })
    return tree

@app.get("/api/tree")
async def read_tree():
    return get_file_tree(DOCS_ROOT)

@app.get("/api/content/{file_path:path}")
async def read_content(file_path: str):
    base_path = (DOCS_ROOT / file_path).resolve()
    
    # Security check: ensure path is within DOCS_ROOT
    if not str(base_path).startswith(str(DOCS_ROOT.resolve())):
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Try the path as is, then with .md, then with .txt
    full_path = base_path
    if not full_path.exists() or not full_path.is_file():
        if (base_path.with_suffix('.md')).exists():
            full_path = base_path.with_suffix('.md')
        elif (base_path.with_suffix('.txt')).exists():
            full_path = base_path.with_suffix('.txt')
        else:
            raise HTTPException(status_code=404, detail="File not found")
        
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
            # If it's a .txt file, wrap it in a markdown code block for better rendering
            if full_path.suffix == '.txt':
                content = f"```text\n{content}\n```"
            return {"content": content, "title": full_path.stem}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount built frontend
if VIEWER_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(VIEWER_DIST / "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # If it's an API call or looks like a static asset, let FastAPI handle or error
        if full_path.startswith("api/") or "." in full_path.split("/")[-1]:
            # This is a bit simplistic, but usually fine for docs
            pass 
            
        index_file = VIEWER_DIST / "index.html"
        if index_file.exists():
            with open(index_file, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read(), status_code=200)
        return {"message": "Documentation server is running. UI built but index.html missing."}
else:
    @app.get("/{full_path:path}")
    async def root(full_path: str):
        return {"message": "Documentation server is running. UI not built yet.", "api": "/api/tree"}

def start_docs_server(port: int = 5055):
    """Entry point for CLI runner"""
    print(f"🚀 Starting Internal Documentation Server on http://127.0.0.1:{port}")
    uvicorn.run(app, host="127.0.0.1", port=port)

if __name__ == "__main__":
    start_docs_server()
