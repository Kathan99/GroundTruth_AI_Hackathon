from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agent import SupportAgent
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="Hyper-Personalized Customer Support Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = SupportAgent()

class ChatRequest(BaseModel):
    user_id: str
    query: str
    latitude: float
    longitude: float

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = agent.process_query(
            user_id=request.user_id,
            query=request.query,
            lat=request.latitude,
            lon=request.longitude
        )
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
