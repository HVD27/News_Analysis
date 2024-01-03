from fastapi import FastAPI, HTTPException
import requests
from newsdataapi import NewsDataApiClient

app = FastAPI()

NEWS_API_KEY = 'pub_35771310a2d3c42f4cc117062a6dfcdbda526'  
def get_top_news(city):

    api = NewsDataApiClient(apikey=NEWS_API_KEY)

    try:
        response = api.news_api( q= f"{city} news" , size=5, country = "us")
        return response['top_articles']['results']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the News API"}

@app.get("/top_articles/{city}")
def get_top_articles(city: str):
    articles = get_top_news(city)
    return {"top_articles": articles}

if __name__ == "__main__":
    import uvicorn

uvicorn.run(app, host="127.0.0.1", port=8000)
