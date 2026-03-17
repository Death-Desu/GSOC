import random
import json
import os

def inject_noise(clean_file, noise_level=0.1):
    """
    clean_file: path to your 50_samples.jsonl
    noise_level: 0.0 to 1.0 (percent of samples to corrupt)
    """
    if not os.path.exists(clean_file):
        print(f"Error: {clean_file} not found.")
        return None

    with open(clean_file, 'r') as f:
        samples = [json.loads(line) for line in f]
    
    num_to_corrupt = int(len(samples) * noise_level)
    indices = random.sample(range(len(samples)), num_to_corrupt)
    
    for idx in indices:
        # Hard Way: Randomly delete a required key or swap values
        keys = list(samples[idx].keys())
        if keys:
            bad_key = random.choice(keys)
            samples[idx][bad_key] = "CORRUPTED_DATA_STRESS_TEST"
            
    # Save as a new Modelfile source
    output_name = f"stressed_{int(noise_level*100)}.jsonl"
    with open(output_name, 'w') as f:
        for s in samples:
            f.write(json.dumps(s) + '\n')
    
    print(f"✅ Generated {output_name} with {int(noise_level*100)}% noise.")
    return output_name

if __name__ == "__main__":
    # Generate a 20% noise dataset for stress-testing the Modelfile resilience
    inject_noise("50_samples.jsonl", 0.2)
