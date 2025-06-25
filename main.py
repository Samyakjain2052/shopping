from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(title="Indian Clothing Image Search API")

# Optional: allow frontend (e.g., React or Streamlit) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UNSPLASH_ACCESS_KEY = "pvf2YcjaJyXB2EL4ME2T3Wzfsg4asZwplauWmC9kAzc"  # Replace with your key

def search_unsplash(query: str, per_page: int = 9):
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "per_page": per_page,
        "client_id": UNSPLASH_ACCESS_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return [img["urls"]["regular"] for img in data["results"]]
    else:
        return {"error": f"Failed to fetch images: {response.text}"}

@app.get("/search")
def search_images(q: str = Query(..., description="Search query for Indian clothing"), per_page: int = 9):
    """
    Search Unsplash for Indian clothing images by query
    """
    images = search_unsplash(q, per_page)
    return {"query": q, "images": images}
