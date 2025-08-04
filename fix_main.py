#!/usr/bin/env python3
"""Script to remove the duplicate main function from main.py"""

# Read the file
with open('main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Original file has {len(lines)} lines")

# Find the duplicate main function (starts at line 182, ends at line 313)
# Line numbers are 1-based, so we need to adjust for 0-based indexing
start_line = 181  # Line 182 in 1-based indexing
end_line = 313    # Line 314 in 1-based indexing

print(f"Removing lines {start_line+1} to {end_line}")
print(f"Line {start_line+1}: {repr(lines[start_line])}")
print(f"Line {end_line}: {repr(lines[end_line-1])}")

# Remove the duplicate function
new_lines = lines[:start_line] + lines[end_line:]

print(f"New file will have {len(new_lines)} lines")

# Write the fixed file
with open('main_fixed.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed file written to main_fixed.py")