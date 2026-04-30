from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline import SoftwareCompilerPipeline

# 1. Initialize the API server FIRST
app = FastAPI(title="AI Software Compiler API")

# 2. Allow the frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-software-compiler.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load your engine
compiler = SoftwareCompilerPipeline()

# 4. Define what the frontend will send us
class PromptRequest(BaseModel):
    prompt: str

# 5. Define the endpoint exactly ONCE
@app.post("/generate")
def generate_schema(request: PromptRequest):
    print(f"\n--- API Received Request: {request.prompt} ---")
    try:
        # Try to run the compiler normally
        final_schema = compiler.run(request.prompt)
        
        # Send the perfect JSON back to the frontend
        return final_schema 
        
    except Exception as e:
        # If the compiler throws our specific retry error, send a clean 429 response
        if "completely down" in str(e) or "API" in str(e):
            raise HTTPException(
                status_code=429, 
                detail="Google API Quota Exhausted. The compiler successfully attempted 3 retries before safely aborting."
            )
        # For any other random error, send a clean 500
        raise HTTPException(status_code=500, detail=str(e))