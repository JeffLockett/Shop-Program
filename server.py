from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()
GROK_API_KEY = "your-api-key"  # Ensure this is your xAI API key

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://shop-program.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Jeff's Repair Shop API"}

@app.post("/agent/{agent_type}")
async def process_task(agent_type: str, input_data: str):
    prompts = {
        "diagnostics": f"Diagnose vehicle issue: {input_data}",
        "repairs": f"Provide repair steps for: {input_data}",
        "maintenance": f"List maintenance tasks for: {input_data}",
        "operations": f"Manage shop task: {input_data}"
    }
    if agent_type not in prompts:
        raise HTTPException(status_code=400, detail="Invalid agent type")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.x.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer AAAAAAAAAAAAAAAAAAAAAN4W1AEAAAAAII9fTQCXy6K9%2FzO5H5TfJPz9I9w%3DvkGzGprD7Ww2b0HLkD8vfCiOZ6WGokkJfezarEXOQbpGWmSe9R", "Content-Type": "application/json"},
            json={
                "model": "grok-3-beta",
                "messages": [{"role": "user", "content": prompts[agent_type]}],
                "max_tokens": 500
            }
        )
        return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)