import subprocess
import json
import sys

# Ensure UTF-8 output if possible
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Actual issues from IntelOwl repo
TEST_CASES = [
    {
        "issue_id": "2480",
        "prompt": "Fix the MISP connector. It is currently failing when sending large JSON bodies. Generate the correct Python requests code.",
        "must_contain": "requests.post"
    },
    {
        "issue_id": "2737",
        "prompt": "The analyzer fails due to 'version mismatch' in IntelOwl dependencies. Resolve the version conflict for Django 4.x.",
        "must_contain": "django>=4.0"
    }
]

def verify_model(model_name):
    print(f"--- Verifying Model: {model_name} ---")
    for case in TEST_CASES:
        print(f"Running Issue {case['issue_id']}...")
        # Calling Ollama via CLI with explicit encoding
        cmd = ["ollama", "run", model_name, case["prompt"]]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            output = result.stdout.lower()
            
            if case["must_contain"] in output:
                status = "PASS"
            else:
                status = "FAIL"
                print(f"DEBUG: Output for {case['issue_id']} did not contain '{case['must_contain']}'")
                print("--- START OUTPUT ---")
                print(result.stdout)
                print("--- END OUTPUT ---")
            
            print(f"Issue {case['issue_id']}: {status}")
        except Exception as e:
            print(f"Error running issue {case['issue_id']}: {e}")

if __name__ == "__main__":
    # Run against our Alpha model
    verify_model("aephi")
