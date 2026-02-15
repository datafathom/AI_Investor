"""
Enrich Route documentation with data from:
1. Audit Results (verification status)
2. Source Code (imports, components, TODOs)
3. Phase Implementation Plans (structured constraints) - Recursive Scan
4. Planning Chat Thread (conceptual context)
"""
import json
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIT_ROOT = PROJECT_ROOT / "DEBUGGING" / "FrontEndAudit" / "results"
DOCS_ROOT = PROJECT_ROOT / "docs" / "frontend" / "routes" / "depts"
SRC_ROOT = PROJECT_ROOT / "Frontend" / "src" / "pages" / "workstations"
PLANS_ROOT = PROJECT_ROOT / "docs" / "_PLANS"
CHAT_THREAD_FILE = PLANS_ROOT / "planning_chat_thread.txt"

# -----------------------------------------------------------------------------
# 1. DATA LOADING & PARSING
# -----------------------------------------------------------------------------

def load_all_plans():
    """
    Recursively parse all Implementation Plans in docs/_PLANS.
    Returns: dict[identifier] -> { title, description, requirements, phase }
    """
    planning_map = {}
    if not PLANS_ROOT.exists(): return planning_map

    # Find all md files that look like implementation plans
    plan_files = list(PLANS_ROOT.rglob("*Implementation*.md"))
    
    print(f"Found {len(plan_files)} implementation plans.")

    for plan_file in plan_files:
        try:
            content = plan_file.read_text(encoding="utf-8")
            phase_name = plan_file.stem.replace("_Implementation_Plan", "").replace("_", " ")
            if "Phase" not in phase_name: phase_name = f"Plan: {phase_name}"

            # Split by Deliverable
            # Matches ## Deliverable X or ## Deliverable X.Y
            deliverables = re.split(r'^## Deliverable \d+(\.\d+)?: ', content, flags=re.MULTILINE)
            
            # The split list will alternate [preamble, section, section...] 
            # OR [preamble, match_group, section, match_group, section] depending on regex groups
            # Let's simplify and just iterate looking for the header
            
            # Better approach: finditer
            for match in re.finditer(r'^## Deliverable \d+(\.\d+)?: (.*?)\n(.*?)(?=\n## Deliverable|\Z)', content, re.MULTILINE | re.DOTALL):
                title = match.group(2).strip()
                section_body = match.group(3)
                
                # Description
                desc_match = re.search(r'### .*?Description\s+(.*?)\s+###', section_body, re.DOTALL)
                description = desc_match.group(1).strip() if desc_match else ""
                
                # Requirements
                ui_reqs = re.findall(r'- \[ \] (.*)', section_body)
                requirements = [r for r in ui_reqs if len(r) > 10]

                payload = {
                    "source": phase_name,
                    "title": title,
                    "description": description,
                    "requirements": requirements,
                    "context": phase_name
                }
                
                # 1. Map by Component Filename
                # Look for `Name.jsx` or just Name.jsx in table cells
                components = re.findall(r'[`|\s]([a-zA-Z0-9]+\.jsx)[`|\s]', section_body)
                for comp in components:
                     planning_map[comp.strip()] = payload

                # 2. Map by Title Slug (heuristic)
                # "Agent Panel Component" -> "agent-panel"
                slug = title.lower().replace(" component", "").replace(" page", "").replace(" ", "-").strip("-")
                planning_map[slug] = payload
                
                # 3. Map by exact title
                planning_map[title] = payload

        except Exception as e:
            print(f"  [WARN] Failed plan {plan_file.name}: {e}")
            
    return planning_map

def load_chat_thread():
    """
    Parse the monolithic chat thread into department chunks.
    Returns: dict[dept_slug] -> list of context strings
    """
    dept_map = defaultdict(list)
    if not CHAT_THREAD_FILE.exists(): return dept_map

    content = CHAT_THREAD_FILE.read_text(encoding="utf-8")
    

    slug_map = {
        "Orchestrator": "orchestrator", "Architect": "architect", "Data Scientist": "data-scientist",
        "Strategist": "strategist", "Trader": "trader", "Guardian": "guardian",
        "Lawyer": "lawyer", "Auditor": "auditor", "Envoy": "envoy",
        "Physicist": "physicist", "Steward": "steward", "Hunter": "hunter",
        "Sentry": "sentry", "Marketing": "marketing",
        "The Financials": "banker", "The Historian": "historian", "Quality Assurance": "stress-tester",
        "The Developer": "refiner"
    }

    # Split roughly by Emoji Headers
    sections = re.split(r'(🏛️|📐|🧪|📉|💹|🏦|⚖️|🕵️‍♂️|🤝|🧘|🏡|🆕)', content)
    
    current_dept = None
    for i in range(1, len(sections), 2):
        # emoji = sections[i]
        text = sections[i+1] if i+1 < len(sections) else ""
        
        # Determine Dept from first line of text
        first_line = text.strip().split('\n')[0]
        
        found = False
        for key, slug in slug_map.items():
            if key in first_line:
                current_dept = slug
                found = True
                break
        
        if found:
            dept_map[current_dept].append(text)
        elif current_dept:
            dept_map[current_dept].append(text)

    return dept_map

def load_mission_defs():
    """Parse missionModulePlanning.txt for structured Mission definitions."""
    mission_map = {}
    mission_file = PLANS_ROOT / "_Completed" / "2_06_26" / "missionModulePlanning.txt"
    if not mission_file.exists(): return mission_map
    
    content = mission_file.read_text(encoding="utf-8")
    
    # Matches "1. Mission: "Title" (Context)" or similar
    mission_pattern = r'\d+\.\s+Mission:\s+"(.*?)"(?:\s*\((.*?)\))?'
    
    for match in re.finditer(mission_pattern, content):
        title = match.group(1).strip()
        context = match.group(2).strip() if match.group(2) else "General Mission"
        
        # Heuristic to find body: text between this match and next "N. Mission:"
        start = match.end()
        next_match = re.search(r'\d+\.\s+Mission:', content[start:])
        end = start + next_match.start() if next_match else len(content)
        
        body = content[start:end].strip()
        
        # Extract Logic and Action
        logic_match = re.search(r'Agent Logic:\s*(.*?)(?=\n\n|\Z)', body, re.DOTALL)
        action_match = re.search(r'Action:\s*(.*?)(?=\n\n|\Z)', body, re.DOTALL)
        
        logic = logic_match.group(1).strip() if logic_match else "Implement Agent Logic"
        action = action_match.group(1).strip() if action_match else "Implement Action"

        payload = {
            "source": "Mission Module",
            "title": title,
            "description": f"**Mission: {title}**\n\n{body[:200]}...",
            "requirements": [f"Logic: {logic}", f"Action: {action}"],
            "context": f"Mission: {title} ({context})"
        }
        
        # Map by Exact Title, Slug, and Context words
        mission_map[title] = payload
        slug = title.lower().replace(" ", "-").replace("'", "")
        mission_map[slug] = payload
        
        # Heuristic: Map "The Backtest Autopilot" to "backtest"
        simple_slug = slug.replace("the-", "").replace("-agent", "").replace("-mission", "")
        mission_map[simple_slug] = payload
        
        # Add keywords for fuzzy matching in main loop
        payload["keywords"] = set(title.lower().split()) - {"the", "a", "an", "agent", "mission", "to", "for"}

    return mission_map

def load_venn_context():
    """Parse venn_dept_agents.txt for Departmental Intersections."""
    venn_map = {}
    venn_file = PLANS_ROOT / "_Completed" / "2_5_26" / "venn_dept_agents.txt"
    if not venn_file.exists(): return venn_map
    
    content = venn_file.read_text(encoding="utf-8")
    
    # Matches "1. [Top-Left] The Orchestrator: "The System Pulse""
    # Group 1: Dept Name, Group 2: Theme
    pattern = r'\d+\.\s+\[.*?\]\s+(.*?):\s+"(.*?)"'
    
    for match in re.finditer(pattern, content):
        dept_name = match.group(1).strip() # e.g. "The Orchestrator"
        theme = match.group(2).strip()
        
        # Find widget list
        start = match.end()
        next_match = re.search(r'\d+\.\s+\[', content[start:])
        end = start + next_match.start() if next_match else len(content)
        body = content[start:end].strip()
        
        widgets = re.findall(r'Widget \d+ \((.*?)\):\s+(.*)', body)
        requirements = [f"Widget: {w[0]} - {w[1]}" for w in widgets]
        
        # Map to "orchestrator" from "The Orchestrator"
        key = dept_name.lower().replace("the ", "").replace(" ", "-")
        
        venn_map[key] = {
            "source": "Venn Diagram Plan",
            "title": theme,
            "description": f"**System Role**: {theme}\n\n{body.split('Widget')[0].strip()}",
            "requirements": requirements,
            "context": f"Venn Plan: {dept_name}"
        }
        
    return venn_map

# -----------------------------------------------------------------------------
# 2. SOURCE & AUDIT ANALYSIS
# -----------------------------------------------------------------------------

def get_file_for_slug(dept_slug, page_slug, src_dir):
    """Find matching JSX file."""
    if not src_dir.exists(): return None
    
    dept_pascal = "".join(word.title() for word in dept_slug.split("-"))
    page_pascal = "".join(word.title() for word in page_slug.split("-"))
    
    candidates = [
        f"{dept_pascal}{page_pascal}.jsx",
        f"{page_pascal}.jsx",
        f"{dept_pascal}{page_slug.replace('-', '').title()}.jsx", # BankerCryptoWallet.jsx
    ]
    
    for name in candidates:
        if (src_dir / name).exists(): return src_dir / name
        
    # Fuzzy
    parts = page_slug.split("-")
    best_match = None
    max_score = 0
    
    for f in src_dir.glob("*.jsx"):
        score = sum(1 for p in parts if p in f.name.lower())
        if score > max_score:
            max_score = score
            best_match = f
            
    return best_match if max_score >= len(parts) - 1 else None

def analyze_source_file(filepath):
    try:
        content = filepath.read_text(encoding="utf-8")
        return {
            "imports": [i for i in re.findall(r'import\s+.*?from\s+[\'"](.+?)[\'"]', content) if not i.startswith(".")],
            "components": sorted(list(set(re.findall(r'<([A-Z][a-zA-Z0-9]+)', content)))),
            "todos": re.findall(r'TODO:?\s*(.*)', content, re.IGNORECASE),
            "lines": len(content.splitlines()),
            "hooks": sorted(list(set(re.findall(r'(use[A-Z][a-zA-Z0-9]+)', content))))
        }
    except:
        return None

# -----------------------------------------------------------------------------
# 3. CONTENT GENERATION
# -----------------------------------------------------------------------------


def generate_overview(dept_slug, page_slug, current_text, chat_context):
    """Generate rich overview using Chat Thread context if available."""
    best_snippet = ""
    
    # 1. Try Specific Page Match
    if chat_context:
        current_text_lower = current_text.lower()
        keywords = page_slug.replace("-", " ").split()
        
        # Filter generic keywords
        stop_words = {"the", "page", "dashboard", "component", "view", "panel"}
        meaningful_keywords = [k for k in keywords if k not in stop_words]
        
        candidates = []
        
        for text_block in chat_context:
            score = 0
            block_lower = text_block.lower()
            
            # Title Match (High Value)
            if page_slug.replace("-", " ") in block_lower: 
                score += 10
            
            # Keyword Match
            matched_keywords = [k for k in meaningful_keywords if k in block_lower]
            score += len(matched_keywords) * 2
            
            if score >= 2: # Lowered threshold (was > 2)
                 candidates.append((score, text_block))

        # Sort by score descending
        candidates.sort(key=lambda x: x[0], reverse=True)
        
        if candidates:
            # Pick the best block's best paragraph
            best_block = candidates[0][1]
            paragraphs = best_block.split('\n\n')
            for p in paragraphs:
                # Find the paragraph with the keywords
                if any(k in p.lower() for k in meaningful_keywords):
                    if len(p) > len(best_snippet):
                        best_snippet = p.strip()
            
            # If no specific paragraph matched well, just take the first substantial one from the block
            if not best_snippet and len(best_block) > 20:
                best_snippet = best_block.split('\n\n')[0].strip()

    # 2. Fallback: Department generic description from Chat Thread
    if not best_snippet and chat_context:
        # Usually the first entry in chat_context for a dept is the high level description
        # We try to use that if it's descriptive
        if len(chat_context) > 0 and len(chat_context[0]) > 50:
             best_snippet = f"**From the System Philosophy:**\n\n{chat_context[0].split('I.')[0].strip()}"

    if best_snippet and len(best_snippet) > 20:
        clean_snippet = best_snippet.replace("I. ", "").replace("II. ", "").strip()
        return f"{clean_snippet}\n\n*(Derived from System Philosophy)*"

    # 3. Last Resort: Template (only if current text is the REALLY old placeholder)
    # The user complained about "just execution.md", so we want to avoid the template if possible.
    # But if we have NOTHING?
    if len(current_text.split('.')) < 3:
        dept_title = dept_slug.replace("-", " ").title()
        page_title = page_slug.replace("-", " ").title()
        return (
            f"The **{page_title}** is a core operational module for the {dept_title}. "
            f"It functions as a specialized workstation for {page_title.lower()} tasks, "
            f"bridging the gap between automated backend processes and human oversight. "
            f"By aggregating {dept_title}-specific metrics, this interface ensures high-fidelity "
            f"situational awareness and rapid execution capabilities within the Sovereign OS grid."
        )
    
    return current_text

# -----------------------------------------------------------------------------
# 4. MAIN LOOP
# -----------------------------------------------------------------------------

def main():
    print("Loading data sources...")
    planning_map = load_all_plans()
    chat_data = load_chat_thread()
    mission_data = load_mission_defs()
    venn_data = load_venn_context()
    
    # Merge Mission Data into Planning Map (Priority to Missions for specific agents)
    for k, v in mission_data.items():
        if k not in planning_map:
            planning_map[k] = v
            
    print(f"Loaded {len(planning_map)} plan items (incl. {len(mission_data)} missions), {len(chat_data)} dept contexts, {len(venn_data)} venn contexts.")
    # Audit Data Loading
    audit_map = {}
    if AUDIT_ROOT.exists():
        for res_dir in AUDIT_ROOT.iterdir(): 
            if res_dir.is_dir():
                files = sorted(list(res_dir.glob("*_verify_results.json")))
                if files: audit_map[res_dir.name.replace("_results","")] = files[-1]


    for dept_dir in DOCS_ROOT.iterdir():
        if not dept_dir.is_dir(): continue
        dept_slug = dept_dir.name.replace("_routes", "")
        
        # Load Audit Status
        route_status = {}
        if dept_slug in audit_map:
            try:
                data = json.loads(audit_map[dept_slug].read_text(encoding="utf-8"))
                route_status = {item["route"]: item["status"] for item in data}
            except: pass

        src_dir = SRC_ROOT / dept_slug
        
        for doc_file in dept_dir.glob("*.md"):
            if doc_file.name.startswith("_"): continue
            
            page_slug = doc_file.stem
            # print(f"Enriching {dept_slug}/{page_slug}...")
            
            # --- 1. RESOLVE DATA ---
            src_file = get_file_for_slug(dept_slug, page_slug, src_dir)
            src_info = analyze_source_file(src_file) if src_file else None
            
            # Plan Lookups
            plan_info = None
            if src_file:
                plan_info = planning_map.get(src_file.name)
            
            if not plan_info:
                plan_info = planning_map.get(page_slug)
            
            # Mission Fallback (Keyword Match if slug fails)
            if not plan_info:
                page_keywords = set(page_slug.split("-"))
                for mission_title, mission_payload in mission_data.items():
                    if "keywords" in mission_payload:
                        intersection = page_keywords & mission_payload["keywords"]
                        if len(intersection) >= 2 or (len(page_keywords) == 1 and len(intersection) == 1):
                            plan_info = mission_payload
                            break
                
            # If still no plan, check components used in source
            if not plan_info and src_info:
                for comp in src_info["components"]:
                    if f"{comp}.jsx" in planning_map:
                        plan_info = planning_map[f"{comp}.jsx"]
                        break

            # Audit Status
            path = f"/{dept_slug}/{page_slug}"
            status = route_status.get(path, "UNKNOWN")
            if status == "UNKNOWN": # Suffix match fallback
                for k, v in route_status.items():
                    if k.endswith(f"/{page_slug}"): status = v
            
            icon = "🟢" if status == "SUCCESS" else "🔴"
            if status == "CONTENT_EMPTY": icon = "🟡"

            # --- 2. BUILD CONTENT ---
            try:
                content = doc_file.read_text(encoding="utf-8")
                
                # UPDATE OVERVIEW
                overview_match = re.search(r'## Overview\s+(.*?)\s+---', content, re.DOTALL)
                if overview_match:
                    current_ov = overview_match.group(1).strip()
                    # Priority: Plan Desc > Chat Context > Template
                    if plan_info and plan_info["description"] and len(plan_info["description"]) > 20:
                        new_ov = plan_info["description"]
                    else:
                        new_ov = generate_overview(dept_slug, page_slug, current_ov, chat_data.get(dept_slug))
                    content = content.replace(current_ov, new_ov)

                # UPDATE METADATA
                content = re.sub(r'\| Implementation \| .*? \|', f'| Implementation | {icon} {status} |', content)
                if src_file:
                    rel_path = src_file.relative_to(PROJECT_ROOT).as_posix()
                    content = re.sub(r'\| Component File \| .*? \|', f'| Component File | `{rel_path}` |', content)
                
                # UPDATE COMPONENTS
                if src_info and src_info["components"]:
                     comps = "\n".join([f"- `{c}`" for c in src_info["components"]])
                     content = re.sub(r'(### UI Components Used\s+).*?(### Data Flow)', f"\\1\n{comps}\n\n\\2", content, flags=re.DOTALL)

                # UPDATE PLANNING
                new_plan = ""
                if plan_info and plan_info["requirements"]:
                    new_plan += f"> **Derived from {plan_info['context']}**\n\n"
                    new_plan += "\n".join([f"- [ ] {r}" for r in plan_info["requirements"]]) + "\n"
                
                if src_info and src_info["todos"]:
                    new_plan += "\n**Code TODOs:**\n" + "\n".join([f"- [ ] {t}" for t in src_info["todos"]]) + "\n"
                
                if not new_plan:
                    new_plan = (
                        "- [ ] **Integrate Real Data**: Replace mock data with live hooks.\n"
                        "- [ ] **Error Boundaries**: Wrap component to prevent crashes.\n"
                        "- [ ] **Loading States**: Add skeletons for async operations.\n"
                        "- [ ] **Responsive Check**: Verify layout on mobile/tablet views."
                    )
                
                # Inject Plan
                content = re.sub(r'(### MVP Requirements\s+\n\n).*?(### Enhanced Features)', f"\\1{new_plan}\n\n\\2", content, flags=re.DOTALL)

                # UPDATE STATS & ANALYSIS
                if src_info:
                    stats = f"> **Source Stats**: {src_info['lines']} lines, {len(src_info['hooks'])} hooks"
                    if "Source Stats" in content:
                        content = re.sub(r'> \*\*Source Stats\*\*: .*', stats, content)
                    else:
                        content = re.sub(r'(> \*\*Route\*\*: .*?)', f"\\1\n\n{stats}", content)
                
                    analysis = "## Detailed Analysis\n\n### Key Imports\n" + \
                               ("\n".join([f"- `{i}`" for i in src_info["imports"][:15]]) if src_info["imports"] else "- None") + \
                               "\n\n### Hooks Used\n" + \
                               ("\n".join([f"- `{h}`" for h in src_info["hooks"]]) if src_info["hooks"] else "- None")
                    
                    if "## Detailed Analysis" in content:
                         content = re.sub(r'## Detailed Analysis.*', analysis, content, flags=re.DOTALL)
                    else:
                         content += "\n\n" + analysis

                doc_file.write_text(content, encoding="utf-8")

            except Exception as e:
                print(f"Failed to update {doc_file.name}: {e}")

    print("Done enrichment.")

if __name__ == "__main__":
    main()
