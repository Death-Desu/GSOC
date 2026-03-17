import os
import json

# Settings
RAW_DIR = "datasets/raw/"
OUTPUT_FILE = "50_samples.jsonl"
INSTRUCTION = "Analyze the security data and return a structured IntelOwl JSON."

def prepare_jsonl():
    samples = []
    
    # Get all .json files from RAW_DIR
    files = [f for f in os.listdir(RAW_DIR) if f.endswith('.json')]
    
    # Take first 50
    for filename in sorted(files)[:50]:
        with open(os.path.join(RAW_DIR, filename), 'r') as f:
            raw_data = json.load(f)
            
            # Simple heuristic for expected output (Normalizing)
            # This simulates the "Senior AI Researcher" refinement for now
            vendor = raw_data.get('vendor', 'unknown')
            
            # Extract name
            name = raw_data.get('ipAddress') or raw_data.get('ip_str') or raw_data.get('ip') or raw_data.get('target', 'unknown')
            if 'data' in raw_data and 'attributes' in raw_data['data']:
                name = raw_data['data']['attributes'].get('id', name)
                
            # Extract score
            score = raw_data.get('abuseConfidenceScore') or raw_data.get('score') or 0
            if 'data' in raw_data and 'attributes' in raw_data['data']:
                stats = raw_data['data']['attributes'].get('last_analysis_stats', {})
                score = stats.get('malicious', score)
            
            # Identify type
            type_val = raw_data.get('type', 'ip')
            
            output_json = {
                "observable_name": name,
                "observable_type": type_val,
                "malicious_score": score,
                "vendor_name": vendor
            }
            
            samples.append({
                "instruction": INSTRUCTION,
                "input": json.dumps(raw_data),
                "output": json.dumps(output_json)
            })
            
    with open(OUTPUT_FILE, 'w') as f:
        for s in samples:
            f.write(json.dumps(s) + "\n")
            
    print(f"✅ Prepared {len(samples)} samples in {OUTPUT_FILE}")

if __name__ == "__main__":
    prepare_jsonl()
