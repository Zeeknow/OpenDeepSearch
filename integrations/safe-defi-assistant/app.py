from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define request body model
class QueryRequest(BaseModel):
    text: str

@app.post("/query")
async def query(request: QueryRequest):
    # request.text gives the input
    user_input = request.text
    
    # 👇 put your logic here
    response = f"Received: {user_input}"
    
    return {"response": response}
