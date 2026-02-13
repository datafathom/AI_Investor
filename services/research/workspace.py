import logging
import uuid
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from services.research.notebook_runner import NotebookRunner

logger = logging.getLogger(__name__)

class ResearchWorkspace:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResearchWorkspace, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.runner = NotebookRunner()
        self.notebooks: Dict[str, Dict] = {}
        self._seed_notebooks()
        self._initialized = True

    def _seed_notebooks(self):
        # Create a sample notebook
        nb_id = str(uuid.uuid4())
        self.notebooks[nb_id] = {
            "id": nb_id,
            "name": "Market Analysis - Q1 2026",
            "cells": [
                {
                    "id": "cell_1",
                    "type": "markdown",
                    "content": "# Market Analysis\nAnalyzing the impact of rate cuts on tech stocks."
                },
                {
                    "id": "cell_2",
                    "type": "code",
                    "content": "import random\nprint('Simulating market data...')\nprices = [random.uniform(100, 200) for _ in range(10)]\nprint(f'Prices: {prices}')"
                }
            ],
            "created_at": datetime.now().isoformat(),
            "modified_at": datetime.now().isoformat()
        }

    async def list_notebooks(self) -> List[Dict]:
        return list(self.notebooks.values())

    async def create_notebook(self, name: str) -> Dict:
        nb_id = str(uuid.uuid4())
        notebook = {
            "id": nb_id,
            "name": name,
            "cells": [],
            "created_at": datetime.now().isoformat(),
            "modified_at": datetime.now().isoformat()
        }
        self.notebooks[nb_id] = notebook
        return notebook

    async def get_notebook(self, id: str) -> Optional[Dict]:
        return self.notebooks.get(id)

    async def save_notebook(self, id: str, notebook: Dict) -> Optional[Dict]:
        if id in self.notebooks:
            notebook['modified_at'] = datetime.now().isoformat()
            self.notebooks[id] = notebook
            return notebook
        return None

    async def execute_cell(self, notebook_id: str, code: str) -> Dict:
        # Use notebook ID as kernel ID to persist state per notebook
        return await self.runner.execute_cell(notebook_id, code)

    async def restart_kernel(self, notebook_id: str):
        await self.runner.restart_kernel(notebook_id)
