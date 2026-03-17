import ollama
import json
import os
import time
from ollama import Client
from aegis_schemas.intelowl_schema import IntelOwlObservable

client = Client(host='http://127.0.0.1:11434')
DATASET_PATH = 'datasets/raw/'

def run_inference(model_name, raw_input):
    system_prompt = (
    "You are a JSON transformer for IntelOwl security platform.\n\n"
    "INPUT: Raw JSON from a security API\n"
    "OUTPUT: Must use EXACTLY these field names (no variations):\n"
    '  - "observable_name" (string): The IP, domain, or hash being analyzed\n'
    '  - "observable_type" (string): One of: "ip", "domain", "url", "hash", "email"\n'
    '  - "malicious_score" (integer 0-100 or null)\n'
    '  - "vendor_name" (string): Source of the data\n\n'
    "EXAMPLES:\n"
    'Input: {"ip_str": "8.8.8.8", "score": 45}\n'
    'Output: {"observable_name": "8.8.8.8", "observable_type": "ip", "malicious_score": 45, "vendor_name": "example"}\n\n'
    'Input: {"domain": "google.com", "reputation": 90}\n'
    'Output: {"observable_name": "google.com", "observable_type": "domain", "malicious_score": 90, "vendor_name": "example"}\n\n'
    "ABSOLUTE RULES:\n"
    "1. Field names must be EXACTLY as shown above\n"
    "2. Use double quotes, not single quotes\n"
    "3. Return ONLY the JSON object, no other text"
    )
    
    start_time = time.time()
    try:
        response = client.chat(
            model=model_name,
            format='json', # Forces Ollama to constrain decoding to JSON
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f"INPUT: {json.dumps(raw_input)}"}
            ],
            options={'temperature': 0} # Deterministic output
        )
        latency = time.time() - start_time
        return response['message']['content'], latency
    except Exception as e:
        return str(e), 0

if __name__ == "__main__":
    models = ['phi3:mini', 'llama3.2', 'research-alpha-50']
    stats = {model: {"pass": 0, "fail": 0, "latencies": []} for model in models}

    for filename in sorted(os.listdir(DATASET_PATH)):
        if not filename.endswith('.json'): continue
        
        with open(os.path.join(DATASET_PATH, filename), 'r') as f:
            raw_sample = json.load(f)

        print(f"\n--- Testing: {filename} ---")
        for model in models:
            raw_output, lat = run_inference(model, raw_sample)
            try:
                # Direct parse - 'format=json' handles the noise
                parsed = json.loads(raw_output)
                validated = IntelOwlObservable(**parsed)
                
                print(f"✅ {model.ljust(10)} | PASS | Latency: {lat:.2f}s")
                stats[model]["pass"] += 1
                stats[model]["latencies"].append(lat)
            except Exception as e:
                print(f"❌ {model.ljust(10)} | FAIL | AI Sent: {raw_output[:50]}...")
                print(f"   Reason: {str(e)[:60]}")
                stats[model]["fail"] += 1

    print("\n" + "="*50)
    print("FINAL AEGIS-BENCH RESEARCH SUMMARY (v2.0 - Alias Aware)")
    print("="*50)
    for m, d in stats.items():
        total = d["pass"] + d["fail"]
        acc = (d["pass"] / total * 100) if total > 0 else 0
        avg_lat = sum(d["latencies"])/len(d["latencies"]) if d["latencies"] else 0
        print(f"{m.ljust(12)} | Accuracy: {acc:>5.1f}% | Avg Latency: {avg_lat:.2f}s")