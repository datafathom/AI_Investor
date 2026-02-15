import os
import re
import json
from pathlib import Path

def get_registry_agents(registry_path: str):
    """Parses agent IDs from departmentRegistry.js using regex."""
    with open(registry_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match agents arrays
    # agents: [ "agent1", "agent2" ]
    agents_blocks = re.findall(r'agents:\s*\[(.*?)\]', content, re.DOTALL)
    all_agents = []
    for block in agents_blocks:
        # Extract quoted strings
        ids = re.findall(r'["\'](.*?)["\']', block)
        all_agents.extend(ids)
    
    # Map departments (very rough since we just need the IDs)
    # Actually, let's extract department by department for better reporting
    dept_blocks = re.findall(r'(\d+):\s*\{(.*?)\n\s*\},', content, re.DOTALL)
    dept_map = {}
    for dept_id, dept_content in dept_blocks:
        name_match = re.search(r'name:\s*["\'](.*?)["\']', dept_content)
        name = name_match.group(1) if name_match else f"Dept {dept_id}"
        
        agents_match = re.search(r'agents:\s*\[(.*?)\]', dept_content, re.DOTALL)
        agents = re.findall(r'["\'](.*?)["\']', agents_match.group(1)) if agents_match else []
        
        dept_map[name] = agents
        
    return dept_map

def get_implemented_agents(agents_dir: str):
    """Lists all Agent classes in .py files."""
    implemented = set()
    for root, _, files in os.walk(agents_dir):
        for file in files:
            if file.endswith('.py'):
                path = Path(root) / file
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Match class XAgent(BaseAgent)
                    classes = re.findall(r'class\s+(\w+Agent)\(BaseAgent\)', content)
                    implemented.update(classes)
    return implemented

def get_documented_agents(docs_dir: str):
    """Lists all agent docs in .md files."""
    documented = set()
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                # Strip extension and focus on the name
                name = file.replace('.md', '').replace('_agent', '').replace('_agents', '')
                documented.add(name.lower())
    return documented

def main():
    root = Path(__file__).parent.parent
    registry_path = root / "Frontend" / "src" / "config" / "departmentRegistry.js"
    agents_dir = root / "agents"
    docs_dir = root / "docs" / "agents"
    
    print("Starting Agent Integrity Audit...")
    
    dept_map = get_registry_agents(str(registry_path))
    implemented = get_implemented_agents(str(agents_dir))
    documented = get_documented_agents(str(docs_dir))
    
    # Normalize implemented for matching (Case insensitive, strip Agent suffix)
    # e.g. LifeCycleModelerAgent -> lifecycle_modeler
    # Normalize for matching (Case insensitive, strip _agent suffix)
    def normalize(name: str):
        # Convert CamelCase to snake_case
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        snake = re.sub('([a-z0-0])([A-Z])', r'\1_\2', s1).lower()
        return snake.replace('_agent', '').strip('_')

    norm_implemented = {normalize(i): i for i in implemented}
    
    report = []
    report.append("# Agent Integrity Audit Results\n")
    report.append("| Department | Registry ID | Source Status | Docs Status |")
    report.append("| :--- | :--- | :--- | :--- |")
    
    total_agents = 0
    missing_code = 0
    missing_docs = 0
    
    for dept, agents in dept_map.items():
        for agent_id in agents:
            total_agents += 1
            # Check code
            # Normalize registry ID too
            norm_id = normalize(agent_id)
            code_found = "✅" if norm_id in norm_implemented or agent_id.lower() in [i.lower() for i in implemented] else "❌ Missing"
            if code_found == "❌ Missing":
                missing_code += 1
                
            # Check docs
            doc_found = "✅" if norm_id.replace('_', '') in [d.replace('_', '').replace('agent', '') for d in documented] else "❌ Missing"
            if doc_found == "❌ Missing":
                missing_docs += 1
            
            report.append(f"| {dept} | `{agent_id}` | {code_found} | {doc_found} |")

    print(f"\nAudit Complete.")
    print(f"Total Agents in Registry: {total_agents}")
    print(f"Missing in Source Code: {missing_code}")
    print(f"Missing in Documentation: {missing_docs}")
    
    report.append(f"\n## Summary Metrics")
    report.append(f"- **Total Agents**: {total_agents}")
    report.append(f"- **Missing Implementation**: {missing_code}")
    report.append(f"- **Missing Documentation**: {missing_docs}")
    
    # List missing for easy copy-paste
    report.append(f"\n## Missing Implementation To-Do")
    for dept, agents in dept_map.items():
        missing_in_dept = [a for a in agents if normalize(a) not in norm_implemented and a.lower() not in [i.lower() for i in implemented]]
        if missing_in_dept:
            report.append(f"### {dept}")
            for m in missing_in_dept:
                report.append(f"- [ ] {m}")

    with open(root / "agent_audit_results.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        
    print(f"\nReport written to agent_audit_results.md")

if __name__ == "__main__":
    main()
