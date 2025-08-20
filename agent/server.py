from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from farcaster_agent import app as farcaster_app

class Query(BaseModel):
    message: str

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.post("/farcaster")
def run_farcaster(query: Query):
    inputs = {"messages": [("user", query.message)]}
    result = farcaster_app.invoke(inputs)
    final = result["messages"][-1]
    content = getattr(final, "content", str(final))
    return {"response": content}

if __name__ == "__main__":
    import uvicorn, os

    uvicorn.run(api, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
