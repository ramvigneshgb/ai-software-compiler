from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline import SoftwareCompilerPipeline

# Initialize the API server
app = FastAPI(title="AI Software Compiler API")

# Allow the frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all frontends (for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your engine!
compiler = SoftwareCompilerPipeline()

# Define what the frontend will send us
class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate_schema(request: PromptRequest):
    print(f"\n--- API Received Request: {request.prompt} ---")
    
    # Run your multi-stage pipeline
    final_schema = compiler.run(request.prompt)
    
    # Send the perfect JSON back to the frontend
    return final_schema