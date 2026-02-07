# Backend Service: Singularity (The Self-Improving AI)

## Overview
The **Singularity Service** contains the platform's most advanced AI capabilities: self-training, autonomous code refactoring, and emergent agent behaviors. It has **16 modules** designed for a future where the system can improve itself.

## Core Components (Selected)

### 1. Training Orchestrator (`training_orchestrator.py`)
- **LoRA/QLoRA Fine-Tuning**: Manages local GPU fine-tuning jobs for custom models.
- **Job Queue**: Tracks active training runs and GPU allocation.

### 2. Auto-Refactor (`auto_refactor.py`)
- AI-powered code analysis and improvement suggestions.

### 3. Bug Hunter (`bug_hunter.py`)
- Autonomous bug detection and fix generation.

### 4. Other Key Modules
- `rag_core.py`: Retrieval-Augmented Generation for contextual AI responses.
- `mind_upload.py`: Captures user decision patterns for persona modeling.
- `inference_engine.py`: Local inference for fine-tuned models.
- `defi_sniper.py`: Autonomous DeFi yield optimization.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Mission Control** | Training Status | `training_orchestrator.get_job_status()` | **Missing** |
| **Evolution Dashboard** | Agent Hall of Fame | Various evolution modules | **Implemented** (`EvolutionDashboard.jsx`) |

## Usage Example

```python
from services.singularity.training_orchestrator import TrainingOrchestrator

orchestrator = TrainingOrchestrator()

job = orchestrator.submit_job(
    model_name="llama-3-8b-family-office",
    dataset_path="/data/family_office_qa.jsonl",
    params={"epochs": 3, "lora_rank": 16}
)

print(f"Job Status: {job['status']}")

# Check later
status = orchestrator.get_job_status(job["submitted_at"][:36])
print(f"Progress: {status.get('progress', 'N/A')}")
```
