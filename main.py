from fastapi import FastAPI, Query, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS so Swagger UI works without errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_SOURCE_URL = "https://november7-730026606190.europe-west1.run.app/messages"

@app.get("/search")
def search_messages(q: str = Query(...), page: int = 1, limit: int = 10):
    try:
        # Fetch data from the external API
        response = requests.get(DATA_SOURCE_URL, timeout=20)
        response.raise_for_status()
        data = response.json()

        # Extract the list of messages
        if isinstance(data, dict) and "items" in data:
            data = data["items"]

        if not isinstance(data, list):
            raise ValueError("Unexpected data format")

        # Filter by 'message' or 'user_name' fields
        results = [
            m for m in data
            if q.lower() in m.get("message", "").lower()
            or q.lower() in m.get("user_name", "").lower()
        ]

        # Apply pagination
        start = (page - 1) * limit
        end = start + limit
        return {"results": results[start:end], "total": len(results)}

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="External API timed out")
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str(e))