import time
import csv
from pipeline import SoftwareCompilerPipeline

def run_strict_evaluation():
    compiler = SoftwareCompilerPipeline()
    
    # 3 REAL PRODUCT PROMPTS
    real_prompts = [
        {"type": "Real", "prompt": "Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments. Admins can see analytics."},
        {"type": "Real", "prompt": "Create an e-commerce backend with products, shopping carts, users, inventory tracking, and Stripe payments."},
        {"type": "Real", "prompt": "Design a blog system where writers can create posts, readers can comment, and admins can delete posts."}
    ]

    # 4 EDGE CASES (Vague, Conflicting, Incomplete, Logic Trap)
    edge_cases = [
        {"type": "Edge - Vague", "prompt": "Make a good app that does stuff with data."},
        {"type": "Edge - Conflicting", "prompt": "Build a highly secure banking app where anyone can access the transaction database without logging in."},
        {"type": "Edge - Incomplete", "prompt": "Just give me a database with 5 tables."},
        {"type": "Edge - Logic Trap", "prompt": "Make an app where only guests can ban admins, but admins control everything."}
    ]

    test_suite = real_prompts + edge_cases
    results = []
    print(f"Starting SERIOUS SIGNAL Evaluation ({len(test_suite)} total prompts)...\n")

    for idx, test in enumerate(test_suite):
        prompt_type = test["type"]
        prompt_text = test["prompt"]
        
        print(f"--- Running Test {idx+1}/{len(test_suite)} [{prompt_type}] ---")
        
        start_time = time.time()
        success = False
        error_types_str = "None"
        retries = 0
        
        try:
            compiler.run(prompt_text)
            success = True
            
            # Extract the new tracking metrics we added to pipeline.py
            if hasattr(compiler, 'last_metrics'):
                retries = compiler.last_metrics["retries"]
                if compiler.last_metrics["failures"]:
                    # Dedup the failure types
                    error_types_str = " | ".join(list(set(compiler.last_metrics["failures"])))
                    
        except Exception as e:
            error_types_str = type(e).__name__
            if hasattr(compiler, 'last_metrics'):
                retries = compiler.last_metrics.get("retries", 0)
            
        latency = round(time.time() - start_time, 2)
        
        results.append({
            "Category": prompt_type,
            "Prompt": prompt_text,
            "Success": "YES" if success else "NO",
            "Latency (s)": latency,
            "Retries": retries,
            "Failure Types": error_types_str
        })
        print(f"Result: {'SUCCESS' if success else 'FAILED'} | Latency: {latency}s | Retries: {retries}\n")
        
        # 15 second cooldown to bypass Google Free Tier Rate Limits
        time.sleep(15) 

    # Write to CSV exactly how the rubric asked
    csv_file = "evaluation_metrics.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Category", "Prompt", "Success", "Latency (s)", "Retries", "Failure Types"])
        writer.writeheader()
        writer.writerows(results)

    # Print Final Summary
    successes = sum(1 for r in results if r['Success'] == "YES")
    avg_latency = sum(r['Latency (s)'] for r in results) / len(results)
    avg_retries = sum(r['Retries'] for r in results) / len(results)
    
    print("\n" + "="*50)
    print(" 📊 SERIOUS SIGNAL EVALUATION REPORT")
    print("="*50)
    print(f"Total Tests Run   : {len(test_suite)}")
    print(f"Overall Success   : {successes}/{len(test_suite)} ({(successes/len(test_suite))*100}%)")
    print(f"Average Latency   : {round(avg_latency, 2)} seconds")
    print(f"Avg Retries/Req   : {round(avg_retries, 2)}")
    print("="*50)
    print(f"Data saved to {csv_file}. Open this in Excel for your Loom video!")

if __name__ == "__main__":
    run_strict_evaluation()