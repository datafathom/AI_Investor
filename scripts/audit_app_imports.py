
import re
import sys

APP_PATH = "frontend/src/App.jsx"

def simplify_component_name(name):
    return name.split('.')[0]

def audit_imports():
    try:
        with open(APP_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Find all imports
        # matches: import Component from ...; or const Component = lazy(...)
        defined_symbols = set()
        
        # Standard imports
        import_pattern = re.compile(r'import\s+(?:\{([^}]+)\}|(\w+))\s+from')
        for match in import_pattern.finditer(content):
            if match.group(1): # { A, B }
                for sym in match.group(1).split(','):
                    defined_symbols.add(sym.strip())
            if match.group(2): # Default
                defined_symbols.add(match.group(2).strip())

        # Lazy imports
        lazy_pattern = re.compile(r'const\s+(\w+)\s*=\s*lazy\(')
        for match in lazy_pattern.finditer(content):
            defined_symbols.add(match.group(1).strip())

        # Local definitions (const X = ...)
        const_pattern = re.compile(r'const\s+(\w+)\s*=')
        for match in const_pattern.finditer(content):
            defined_symbols.add(match.group(1).strip())
            
        # Function definitions
        func_pattern = re.compile(r'function\s+(\w+)\(')
        for match in func_pattern.finditer(content):
            defined_symbols.add(match.group(1).strip())

        # 2. Find all used components in JSX
        # element={<Component />} or <Component ... />
        # We look for Capitalized words inside <...>
        
        used_components = set()
        
        # element={<Component />}
        element_pattern = re.compile(r'element=\{<(\w+)')
        for match in element_pattern.finditer(content):
            used_components.add(match.group(1).strip())

        # Direct usage <Component ... />
        jsx_pattern = re.compile(r'<([A-Z]\w+)')
        for match in jsx_pattern.finditer(content):
            used_components.add(match.group(1).strip())

        # Filter out standard React/Router components if they are not explicitly imported but global (unlikely in strict setup)
        # But usually Navigate, Route, Routes etc are imported. 
        # We will check everything.

        missing = []
        for comp in used_components:
            # React Fragment
            if comp == 'React': continue
            
            if comp not in defined_symbols:
                # Double check for standard React/Browser things? 
                # Assuming all custom components must be defined.
                missing.append(comp)

        if missing:
            print("❌ Found Missing Imports/Definitions in App.jsx:")
            for m in missing:
                print(f"  - {m}")
            return False
        else:
            print("✅ All Used Components appear to be Defined/Imported.")
            return True

    except Exception as e:
        print(f"Error auditing file: {e}")
        return False

if __name__ == "__main__":
    success = audit_imports()
    if not success:
        sys.exit(1)
