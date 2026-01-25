"""
Script to generate test file templates for all services to achieve 100% coverage.
This script analyzes the codebase and creates test templates for uncovered code.
"""

import os
import ast
import re
from pathlib import Path
from typing import List, Dict, Set


def find_python_files(directory: str) -> List[Path]:
    """Find all Python files in a directory."""
    files = []
    for root, dirs, filenames in os.walk(directory):
        # Skip test directories and __pycache__
        if 'test' in root or '__pycache__' in root:
            continue
        for filename in filenames:
            if filename.endswith('.py') and not filename.startswith('test_'):
                files.append(Path(root) / filename)
    return files


def extract_class_methods(file_path: Path) -> Dict[str, List[str]]:
    """Extract class names and their methods from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content)
        
        classes = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append(item.name)
                classes[node.name] = methods
        return classes
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return {}


def check_test_exists(service_file: Path, test_dir: Path) -> bool:
    """Check if a test file already exists for a service file."""
    service_name = service_file.stem
    test_file = test_dir / f"test_{service_name}.py"
    return test_file.exists()


def generate_test_template(service_file: Path, classes: Dict[str, List[str]]) -> str:
    """Generate a test file template for a service."""
    service_name = service_file.stem
    module_path = str(service_file).replace(os.sep, '.').replace('.py', '')
    
    template = f'''"""
Tests for {service_file.name}
Generated test template for 100% coverage
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from {module_path} import {', '.join(classes.keys())}


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    # TODO: Add appropriate mocks for dependencies
    pass


'''
    
    # Add test methods for each class and method
    for class_name, methods in classes.items():
        template += f'''
class Test{class_name}:
    """Tests for {class_name} class."""
    
'''
        for method in methods:
            if not method.startswith('_'):
                template += f'''    @pytest.mark.asyncio
    async def test_{method}(self, service):
        """Test {method} method."""
        # TODO: Implement test
        pass

'''
    
    return template


def main():
    """Main function to generate test templates."""
    services_dir = Path('services')
    tests_dir = Path('tests')
    
    # Find all service files
    service_files = find_python_files(str(services_dir))
    
    print(f"Found {len(service_files)} service files")
    
    missing_tests = []
    for service_file in service_files:
        # Get relative path for test file
        rel_path = service_file.relative_to(services_dir)
        test_file_path = tests_dir / rel_path.parent / f"test_{service_file.name}"
        
        if not test_file_path.exists():
            missing_tests.append((service_file, test_file_path))
            print(f"Missing test: {test_file_path}")
    
    print(f"\nFound {len(missing_tests)} missing test files")
    
    # Generate test templates
    for service_file, test_file_path in missing_tests[:10]:  # Limit to first 10 for now
        classes = extract_class_methods(service_file)
        if classes:
            template = generate_test_template(service_file, classes)
            
            # Create directory if needed
            test_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write template
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(template)
            
            print(f"Generated: {test_file_path}")


if __name__ == '__main__':
    main()
