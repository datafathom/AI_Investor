
filepath = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\frontend2\src\App.jsx"

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

brackets = {'(': ')', '[': ']', '{': '}'}
stack = []

for line_num, line in enumerate(lines, 1):
    # Strip comments (roughly)
    stripped = ''
    i = 0
    in_string = False
    quote_char = ''
    while i < len(line):
        char = line[i]
        if not in_string:
            if char in '"\'`':
                in_string = True
                quote_char = char
            elif char == '/' and i + 1 < len(line) and line[i+1] == '/':
                break # Single line comment
            elif char in '({[':
                stack.append((char, line_num, i))
            elif char in ')}]':
                if not stack:
                    print(f"Extra closing '{char}' at line {line_num}, col {i}")
                else:
                    top, t_line, t_col = stack.pop()
                    if brackets[top] != char:
                        print(f"Mismatched '{char}' at line {line_num}, col {i}. Expected '{brackets[top]}' from line {t_line}")
        else:
            if char == quote_char and (i == 0 or line[i-1] != '\\'):
                in_string = False
        i += 1

while stack:
    top, t_line, t_col = stack.pop()
    print(f"Unclosed '{top}' from line {t_line}")
