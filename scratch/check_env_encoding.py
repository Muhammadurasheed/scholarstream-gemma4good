import os

file_path = r'c:\Users\HP\Documents\scholarstream-monorepo\backend\.env'

try:
    with open(file_path, 'rb') as f:
        content = f.read()
    
    print(f"File size: {len(content)} bytes")
    
    # Try to decode as utf-8
    try:
        content.decode('utf-8')
        print("File is valid UTF-8")
    except UnicodeDecodeError as e:
        print(f"UTF-8 decode error: {e}")
        
    # Try to decode as cp1252 (Windows default)
    try:
        content.decode('cp1252')
        print("File is valid CP1252")
    except UnicodeDecodeError as e:
        print(f"CP1252 decode error: {e}")
        # Find where it failed
        pos = e.start
        context = content[max(0, pos-20):min(len(content), pos+20)]
        print(f"Problem byte at pos {pos}: {hex(content[pos])}")
        print(f"Context: {context}")

except Exception as e:
    print(f"Error reading file: {e}")
