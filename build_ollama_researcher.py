import json
import os

# 1. Configuration - The BOM for your model
DATA_SOURCE = "50_samples.jsonl"
MODEL_NAME = "aephi"
BASE_MODEL = "llama3.2" # Using llama3.2 since it's already installed
OUTPUT_FILE = "ResearchBot.Modelfile"

def generate_modelfile():
    # Header of the Modelfile
    modelfile_content = [
        f"FROM {BASE_MODEL}",
        "PARAMETER temperature 0.2",
        "PARAMETER top_p 0.9",
        "SYSTEM 'You are a PhD-level AI Research Assistant. Your responses must be grounded in the provided 50-sample context and prioritize numerical data over prose.'"
    ]

    # 2. Injecting the 50 Samples (The Hard Way)
    if not os.path.exists(DATA_SOURCE):
        print(f"Error: {DATA_SOURCE} not found. Create it first.")
        # Create a dummy sample file for demonstration if it doesn't exist
        with open(DATA_SOURCE, 'w') as f:
            dummy_data = {
                "instruction": "Identify the core 'Atomic Fact' and rewrite the output to be concise, data-driven, and free of conversational fluff.",
                "input": '{"id": "abuse_1", "vendor": "abuseipdb", "ipAddress": "45.3.2.1", "abuseConfidenceScore": 98}',
                "output": '{"observable_name": "45.3.2.1", "observable_type": "ip", "malicious_score": 98, "vendor_name": "abuseipdb"}'
            }
            f.write(json.dumps(dummy_data) + "\n")
        print(f"Created a dummy {DATA_SOURCE} for demonstration.")

    with open(DATA_SOURCE, 'r') as f:
        for line in f:
            if not line.strip(): continue
            try:
                data = json.loads(line)
                # Formatting as few-shot examples for the model's internal state
                inst = data.get("instruction", "")
                inp = data.get("input", "")
                out = data.get("output", "")
                
                combined_input = f"{inst} {inp}".strip()
                modelfile_content.append(f"MESSAGE user '{combined_input}'")
                modelfile_content.append(f"MESSAGE assistant '{out}'")
            except json.JSONDecodeError:
                continue

    # 3. Write to disk
    with open(OUTPUT_FILE, 'w') as f:
        f.write("\n".join(modelfile_content))
    
    print(f"Success: {OUTPUT_FILE} created.")
    print(f"Run this command to build: ollama create {MODEL_NAME} -f {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_modelfile()
