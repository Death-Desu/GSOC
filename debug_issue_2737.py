import subprocess
import sys

cmd = ["ollama", "run", "aephi", "The analyzer fails due to 'version mismatch' in IntelOwl dependencies. Resolve the version conflict for Django 4.x."]
result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

with open("issue_2737_output.txt", "w", encoding='utf-8') as f:
    f.write(result.stdout)

print("Done writing output.")
