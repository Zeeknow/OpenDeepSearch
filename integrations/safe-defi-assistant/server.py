from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request schema
class QueryRequest(BaseModel):
    text: str

# Response schema (optional but nice for docs)
class QueryResponse(BaseModel):
    response: str

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    # Extract user text
    user_input = request.text
    
    # TODO: replace this with your actual pipeline call
    answer = f"Received: {user_input}"
    
    return {"response": answer}
