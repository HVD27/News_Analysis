from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import openai
from newsdataapi import NewsDataApiClient

app = FastAPI()
templates = Jinja2Templates(directory="templates")

NEWS_API_KEY = 'pub_35771310a2d3c42f4cc117062a6dfcdbda526'

def get_top_news(city):

    api = NewsDataApiClient(apikey=NEWS_API_KEY)

    try:
        response = api.news_api( q= f"{city} news" , size=5, country = "us")
        return response['results']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
    
from fastapi import Request

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    message = "Welcome! Use /top_articles/{city} to get top news articles for a specific city."
    return templates.TemplateResponse("index.html", {"request": request, "message": message})

from fastapi import FastAPI, Request, Form
@app.post("/top_articles")
def get_top_articles(request: Request, city: str = Form(...)):
    articles = get_top_news(city)  # Assuming get_top_news is a function that retrieves articles based on the city
    return templates.TemplateResponse("index.html", {"request": request, "city": city, "articles": articles})

if __name__ == "__main__":
    import uvicorn

uvicorn.run(app, host="127.0.0.1", port=8000)
