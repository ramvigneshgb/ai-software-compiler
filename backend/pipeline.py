import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schemas import AppConfiguration

# Load environment variables
load_dotenv()

class SoftwareCompilerPipeline:
    def __init__(self):
        # Initialize the Gemini client
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"

    def stage_1_intent_extraction(self, user_prompt: str) -> str:
        print("-> Stage 1: Extracting Intent...")
        return user_prompt 

    def stage_2_system_design(self, intent_data: str) -> str:
        print("-> Stage 2: Designing System Architecture...")
        system_context = f"Target App: {intent_data}. Needs UI, API, DB, and Auth layers."
        return system_context

    def stage_3_schema_generation(self, system_design: str) -> AppConfiguration:
        print("-> Stage 3: Generating Strict Schemas (Calling Gemini API)...")
        
        prompt = f"""
        You are a compiler for software generation. 
        Based on the following system design, generate a strict, complete, and reliable JSON configuration.
        System Design: {system_design}
        """

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=AppConfiguration,
                        temperature=0.1,
                    ),
                )
                
                raw_json = json.loads(response.text)
                validated_schema = AppConfiguration(**raw_json)
                return validated_schema
                
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    wait_time = (attempt + 1) * 5
                    print(f"   [API Overloaded] Caught 503 Error. Retrying in {wait_time} seconds... (Attempt {attempt + 1} of {max_retries})")
                    time.sleep(wait_time)
                else:
                    raise e
                    
        raise Exception("System Failed: Gemini API is completely down after multiple retries.")

    def stage_4_refinement(self, draft_schema: AppConfiguration) -> AppConfiguration:
        print("-> Stage 4: Running Cross-Layer Validation & Auto-Repair...")
        
        # 1. THE CHECKER: Look for logical inconsistencies
        errors_found = []
        
        # Check A: Do all API roles exist in the Auth roles list?
        defined_roles = draft_schema.auth.roles
        for endpoint in draft_schema.api.endpoints:
            for role in endpoint.allowed_roles:
                if role not in defined_roles:
                    errors_found.append(f"API endpoint {endpoint.path} uses undefined role: '{role}'")

        # Check B: Do all Database foreign keys map to actual tables?
        table_names = [table.name for table in draft_schema.database.tables]
        for table in draft_schema.database.tables:
            for col in table.columns:
                if col.relation and col.relation not in table_names:
                    errors_found.append(f"Table '{table.name}' has invalid relation '{col.relation}' on column '{col.name}'")

        # 2. THE REPAIR ENGINE
        if not errors_found:
            print("   [Validation Passed] No cross-layer inconsistencies found.")
            return draft_schema
            
        print(f"   [Validation Failed] Found {len(errors_found)} logical bugs: {errors_found}")
        print("   [Auto-Repair] Triggering targeted regeneration...")
        
        repair_prompt = f"""
        You are a strict system architect. The following JSON configuration has logical errors.
        Current Configuration: {draft_schema.model_dump_json()}
        
        Fix the following specific errors:
        {errors_found}
        
        Return the entirely repaired JSON configuration. Do not change parts that are already correct.
        """
        
        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=repair_prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=AppConfiguration,
                        temperature=0.1,
                    ),
                )
                repaired_json = json.loads(response.text)
                return AppConfiguration(**repaired_json)
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    wait_time = (attempt + 1) * 5
                    print(f"   [Repair API Overloaded] Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise e
                    
        raise Exception("Failed to repair schema after multiple attempts.")

    def run(self, user_prompt: str):
        print(f"Compiling prompt: '{user_prompt}'\n")
        
        intent = self.stage_1_intent_extraction(user_prompt)
        design = self.stage_2_system_design(intent)
        
        # Execute the LLM call
        draft_schema = self.stage_3_schema_generation(design)
        final_schema = self.stage_4_refinement(draft_schema)
        
        print("\n=== FINAL COMPILED OUTPUT ===")
        print(final_schema.model_dump_json(indent=2))
        return final_schema

if __name__ == "__main__":
    compiler = SoftwareCompilerPipeline()
    compiler.run("Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments. Admins can see analytics.")