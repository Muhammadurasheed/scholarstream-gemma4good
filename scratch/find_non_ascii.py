import os

def find_non_ascii(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for i, line in enumerate(content.splitlines()):
                            for char in line:
                                if ord(char) > 127:
                                    print(f"Non-ASCII at {path}:{i+1} -> {char} (U+{ord(char):04X})")
                                    break
                except Exception as e:
                    print(f"Error reading {path}: {e}")

if __name__ == "__main__":
    find_non_ascii('backend/app')
