from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests
import praw
import openai

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Replace these placeholder values with your actual API keys
reddit_client_id = "9U7VbDvYE8WTRjj6Xz1TQ"
reddit_client_secret = "N4sbj3VWP8fGXWLpNW2ypppQEOZ"
reddit_user_agent = "Sensitive-Beat-7772"
newsdata_api_key = "pub_35771310a2d3c42f4cc117062a6dfcdbda526" 
openai.api_key = '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'

# Task 1: Gather data - Hot Topics from Newsdata API
def get_hot_topics(city, api_key):
    endpoint = "https://newsdata.io/api/1/news"
    params = {
        "apiKey": api_key,
        "q": city,
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)
        top_headlines = [article["title"] for article in data.get("articles", [])]
        return top_headlines
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error")

# Task 2: Gather relevant discussions - Reddit
def get_reddit_discussions(client_id, client_secret, user_agent, topic):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

    try:
        subreddit = reddit.subreddit("all")
        reddit_discussions = subreddit.search(topic, sort="relevance", time_filter="day", limit=10)

        discussions = []
        for submission in reddit_discussions:
            discussions.append({
                "user": submission.author.name,
                "text": submission.title,
                "created_at": submission.created_utc,
            })

        return discussions
    except Exception as e:
        print(f"Error in get_reddit_discussions: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error")

# Task 3: Analyze gathered information - OpenAI GPT-3
def analyze_discussions(discussions):
    summaries = [discussion['text'] for discussion in discussions]

    # Use GPT-3 to generate a summary
    gpt3_summary = generate_gpt3_summary(summaries)

    return {
        "highlights": summaries,
        "gpt3_summary": gpt3_summary
    }

def generate_gpt3_summary(input_texts):
    prompt = "\n".join(input_texts)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# FastAPI routes
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/results")
def read_item(request: Request, city: str = Form(...)):
    try:
        # Task 1: Gathering data - Hot Topics
        hot_topics = get_hot_topics(city, newsdata_api_key)

        if hot_topics:
            # Task 2: Gathering relevant discussions - Reddit, and Task 3: Analyzing gathered information
            discussions_info = []
            for topic in hot_topics:
                reddit_discussions = get_reddit_discussions(
                    reddit_client_id,
                    reddit_client_secret,
                    reddit_user_agent,
                    topic
                )
                if reddit_discussions:
                    # Task 3: Analyzing gathered information
                    discussions_info.extend(analyze_discussions(reddit_discussions))

            return {"city": city, "hot_topics": hot_topics, "discussions_info": discussions_info}
        else:
            
            return "Failed to fetch hot topics. Please check your API keys and network connection."
    except HTTPException as he:
        raise he  # Reraise HTTPException with details
    except Exception as e:
        print(f"Error in read_item: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error")
    
if __name__ == "__main__":
    import uvicorn

uvicorn.run(app, host="127.0.0.1", port=8001)