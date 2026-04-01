import subprocess
import sys

cmd = ["ollama", "run", "aephi", "Fix the MISP connector. It is currently failing when sending large JSON bodies. Generate the correct Python requests code."]
result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

with open("issue_2480_output.txt", "w", encoding='utf-8') as f:
    f.write(result.stdout)

print("Done writing output.")
