import os

def find_unhashable_usage(root_dir):
    keywords = ["set([", "set([[", "dict([", "dict([[", "set(", "dict(", "set({", "dict({"]
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        for keyword in keywords
