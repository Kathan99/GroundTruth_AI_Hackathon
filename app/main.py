from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agent import SupportAgent
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="Velvet Brew Support Agent")

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
    user_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        print(f"Received Request: User={request.user_id}, Lat={request.latitude}, Lon={request.longitude}, Query={request.query}")
        response, final_user_id = agent.process_query(
            user_id=request.user_id,
            query=request.query,
            lat=request.latitude,
            lon=request.longitude
        )
        return ChatResponse(response=response, user_id=final_user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
