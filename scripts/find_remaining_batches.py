
import os
import re

task_path = r'c:\Users\astir\Desktop\AI_Company\AI_Investor\web'
testing_path = r'c:\Users\astir\Desktop\AI_Company\AI_Investor\tests\api'
task_file = r'c:\Users\astir\.gemini\antigravity\brain\9d10b4c0-dbd1-40ad-b0d7-9428c3958bcd\task.md'

with open(task_file, 'r') as f:
    content = f.read()

# Extract all test_*.py mentioned in task.md
matches = re.findall(r'test_\w+\.py', content)
already_listed = set(matches)

# Get all test files in tests/api
all_tests = [f for f in os.listdir(testing_path) if f.startswith('test_') and f.endswith('.py')]
all_tests.sort()

# Filter out already listed
remaining = [f for f in all_tests if f not in already_listed]

# Print remaining files grouped into batches of 15
for i in range(0, len(remaining), 15):
    batch_num = 6 + (i // 15)
    print(f"## Batch {batch_num}:")
    for test_file in remaining[i:i+15]:
        print(f"- [ ] {test_file}")
    print()
