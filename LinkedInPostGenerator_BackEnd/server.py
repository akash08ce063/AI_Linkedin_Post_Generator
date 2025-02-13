from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import uvicorn
from linkedin_post_generator import LinkedInPostGenerator
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


linked_in_post_generator = LinkedInPostGenerator()

# Define the request body structure
class PostRequest(BaseModel):
    type: str
    value: str

# Create an endpoint to generate a LinkedIn post
@app.post("/generate")
async def generate_post(request: PostRequest):
    try:
        post_type = request.type
        post_value = request.value
        
        # Generate the post content
        response = await linked_in_post_generator.generate(post_type, post_value)
        
        # Return the generated post
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Main method to run the app
def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# If this file is run directly, the main function will execute
if __name__ == "__main__":
    main()