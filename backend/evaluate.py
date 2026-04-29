import time
import csv
from pipeline import SoftwareCompilerPipeline

def run_evaluation():
    compiler = SoftwareCompilerPipeline()
    
    # A mix of clear prompts and dirty edge cases
    test_prompts = [
        # Normal Prompts
        "Build a basic to-do list app with users, tasks, and an admin dashboard to see total users.",
        "Create an e-commerce backend with products, shopping carts, users, and Stripe payments.",
        "Design a blog system where writers can create posts, readers can comment, and admins can delete posts.",
        
        # Edge Cases: Vague
        "Make an app like Uber but for dog walking.",
        "I need a system that does stuff with data.",
        
        # Edge Cases: Conflicting
        "Build a secure banking app where anyone can access the transaction database without logging in.",
        
        # Edge Cases: Underspecified
        "Just give me a database with 5 tables."
    ]

    results = []
    print(f"Starting evaluation of {len(test_prompts)} prompts...\n")

    for idx, prompt in enumerate(test_prompts):
        print(f"--- Running Test {idx+1}/{len(test_prompts)} ---")
        print(f"Prompt: {prompt}")
        
        start_time = time.time()
        success = False
        error_type = "None"
        
        try:
            # Run the pipeline
            compiler.run(prompt)
            success = True
        except Exception as e:
            error_type = type(e).__name__
            print(f"FAILED: {e}")
            
        latency = round(time.time() - start_time, 2)
        
        # Log the result
        results.append({
            "prompt": prompt,
            "success": success,
            "latency_seconds": latency,
            "error_type": error_type
        })
        print(f"Result: {'SUCCESS' if success else 'FAILED'} in {latency}s\n")
        
        # Sleep slightly to avoid hitting rate limits instantly
        time.sleep(2)

    # Write to CSV
    csv_file = "evaluation_metrics.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["prompt", "success", "latency_seconds", "error_type"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nEvaluation Complete! Metrics saved to {csv_file}")
    
    # Calculate basic stats
    successes = sum(1 for r in results if r['success'])
    avg_latency = sum(r['latency_seconds'] for r in results) / len(results)
    print(f"Success Rate: {successes}/{len(test_prompts)} ({(successes/len(test_prompts))*100}%)")
    print(f"Average Latency: {round(avg_latency, 2)}s")

if __name__ == "__main__":
    run_evaluation()