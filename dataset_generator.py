import os
import json
import random

def generate_stress_test(num_samples=50):
    os.makedirs('datasets/raw', exist_ok=True)
    
    vendors = ["virustotal", "shodan", "abuseipdb", "greynoise", "internal"]
    
    for i in range(num_samples):
        vendor = random.choice(vendors)
        # Generate random-ish IP
        ip_parts = [str(random.randint(1, 255)) for _ in range(4)]
        ip = ".".join(ip_parts)
        score = random.randint(0, 100)
        
        if vendor == "virustotal":
            sample = {
                "id": f"vt_{i}", 
                "vendor": vendor, 
                "data": {
                    "attributes": {
                        "last_analysis_stats": {"malicious": score, "total": 100}, 
                        "id": ip
                    }
                }
            }
        elif vendor == "shodan":
            sample = {
                "id": f"sho_{i}", 
                "vendor": vendor, 
                "ip_str": ip, 
                "ports": [80, 443], 
                "vulns": [], 
                "score": score
            }
        elif vendor == "abuseipdb":
            sample = {
                "id": f"abuse_{i}", 
                "vendor": vendor, 
                "ipAddress": ip, 
                "abuseConfidenceScore": score
            }
        elif vendor == "greynoise":
            sample = {
                "id": f"grey_{i}", 
                "vendor": vendor, 
                "ip": ip, 
                "classification": "malicious" if score > 50 else "benign"
            }
        else: # internal
            sample = {
                "id": f"min_{i}", 
                "vendor": "internal", 
                "target": ip, 
                "type": "ip", 
                "score": score
            }
            
        with open(f'datasets/raw/sample_{i}.json', 'w') as f:
            json.dump(sample, f, indent=2)
            
    print(f"✅ Generated {num_samples} stress-test samples in datasets/raw/")

if __name__ == "__main__":
    generate_stress_test(50)