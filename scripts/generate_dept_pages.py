import os

pages = [
    (1, "Orchestrator"),
    (2, "Architect"),
    (3, "DataScientist"),
    (4, "Strategist"),
    (5, "Trader"),
    (6, "Physicist"),
    (7, "Hunter"),
    (8, "Sentry"),
    (9, "Steward"),
    (10, "Guardian"),
    (11, "Lawyer"),
    (12, "Auditor"),
    (13, "Envoy"),
    (14, "FrontOffice"),
    (15, "Historian"),
    (16, "StressTester"),
    (17, "Refiner"),
    (18, "Banker")
]

template = """import React from 'react';
import DepartmentDashboard from '../../components/Departments/DepartmentDashboard';

const {name}Page = () => {{
  return <DepartmentDashboard deptId={{{id}}} />;
}};

export default {name}Page;
"""

base_path = "Frontend/src/pages/Departments"

for id, name in pages:
    file_name = f"{name}Page.jsx"
    file_path = os.path.join(base_path, file_name)
    content = template.format(id=id, name=name)
    with open(file_path, "w") as f:
        f.write(content)
    print(f"Created {file_path}")
