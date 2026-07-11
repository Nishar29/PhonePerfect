import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"
js_path = os.path.join(workspace_dir, "app.js")

with open(js_path, "r", encoding="utf-8") as f:
    code = f.read()

# Stack for bracket matching
stack = []
pairs = {
    '}': '{',
    ')': '(',
    ']': '['
}

errors = []
line_num = 1
col_num = 0

# Remove string literals and comments to avoid false positives
clean_code = []
in_single_comment = False
in_multi_comment = False
in_string = None # '"', "'", "`"
escape = False

i = 0
n = len(code)
while i < n:
    char = code[i]
    
    # Track line numbers
    if char == '\n':
        line_num += 1
        col_num = 0
    else:
        col_num += 1

    if escape:
        escape = False
        i += 1
        continue

    if in_single_comment:
        if char == '\n':
            in_single_comment = False
        i += 1
        continue

    if in_multi_comment:
        if char == '*' and i + 1 < n and code[i+1] == '/':
            in_multi_comment = False
            i += 2
        else:
            i += 1
        continue

    if in_string:
        if char == '\\\\':
            escape = True
        elif char == in_string:
            in_string = None
        i += 1
        continue

    # Check comments
    if char == '/' and i + 1 < n and code[i+1] == '/':
        in_single_comment = True
        i += 2
        continue
    if char == '/' and i + 1 < n and code[i+1] == '*':
        in_multi_comment = True
        i += 2
        continue

    # Check strings
    if char in ['"', "'", "`"]:
        in_string = char
        i += 1
        continue

    # Process brackets
    if char in ['{', '(', '[']:
        stack.append((char, line_num, col_num))
    elif char in ['}', ')', ']']:
        if not stack:
            errors.append(f"Unexpected closing '{char}' at line {line_num}, col {col_num}")
        else:
            top_char, top_line, top_col = stack.pop()
            if pairs[char] != top_char:
                errors.append(f"Mismatched closing '{char}' at line {line_num}, col {col_num} (matches '{top_char}' from line {top_line}, col {top_col})")

    i += 1

# Check for leftovers
while stack:
    char, line, col = stack.pop()
    errors.append(f"Unclosed opening '{char}' from line {line}, col {col}")

if errors:
    print("Found matching bracket errors in app.js:")
    for err in errors[:20]:
        print(" -", err)
else:
    print("SUCCESS: Curly braces, brackets, and parentheses are perfectly balanced!")
