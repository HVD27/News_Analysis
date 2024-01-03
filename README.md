# MLexperts_tasks_final
# FastAPI News Aggregator main1.py

This FastAPI application serves as a news aggregator that allows users to retrieve top news articles for a specific city. The application integrates with the NewsDataAPI to fetch news data based on the provided city.

## Project Structure

- **main1.py**: The main FastAPI application file.
- **templates/index.html**: HTML template for rendering the response.

## Dependencies

Make sure to install the required dependencies by running:

```bash
pip install fastapi[all] openai newsdataapi uvicorn
```

## Running the Application

To run the FastAPI application, use the following command:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

This command starts the application locally on `http://127.0.0.1:8000/`.

## Explanation of Code

- **app.py**:

    - **Imports**: The necessary FastAPI modules and external libraries are imported.

    - **Configuration**: The NewsDataAPI key is stored in the `NEWS_API_KEY` variable.

    - **`get_top_news` Function**: This function utilizes the NewsDataAPI to retrieve the top news articles for a given city. It takes a city as a parameter and returns a list of articles.

    - **`read_root` Endpoint**: This endpoint, with a GET request to "/", renders the `index.html` template and provides a welcome message.

    - **`get_top_articles` Endpoint**: This endpoint, with a POST request to "/top_articles", takes a city parameter from a form and calls the `get_top_news` function. It then renders the `index.html` template with the requested city and the retrieved articles.

    - **Application Execution**: The script checks if it is the main module and runs the FastAPI application using the uvicorn server.

## Accessing the Application

Open your web browser and navigate to `http://127.0.0.1:8000/` to access the homepage. The homepage provides a welcome message and instructs users to use the `/top_articles` endpoint to get top news articles for a specific city.


# FastAPI News Analyzer main.py

This FastAPI application serves as a news analyzer that gathers hot topics from the NewsData API, retrieves relevant discussions from Reddit, and uses OpenAI GPT-3 to analyze and generate summaries of the gathered information.

## Project Structure

- **main.py**: The main FastAPI application file.
- **templates/index.html**: HTML template for rendering the response.

## Configuration

Replace the placeholder values in `main.py` with your actual API keys:

- `reddit_client_id`, `reddit_client_secret`, `reddit_user_agent`: Reddit API credentials.
- `newsdata_api_key`: NewsData API key.
- `openai.api_key`: OpenAI GPT-3 API key.

## Dependencies

Make sure to install the required dependencies by running:

```bash
pip install fastapi[all] requests praw openai uvicorn
```

## Running the Application

To run the FastAPI application, use the following command:

```bash
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

This command starts the application locally on `http://127.0.0.1:8001/`.

## Explanation of Code

- **main.py**:

    - **Imports**: The necessary FastAPI modules and external libraries are imported.

    - **Configuration**: API keys for Reddit, NewsData, and OpenAI GPT-3 are provided.

    - **`get_hot_topics` Function**: This function gathers hot topics for a specific city using the NewsData API.

    - **`get_reddit_discussions` Function**: This function retrieves relevant discussions from Reddit based on a given topic.

    - **`analyze_discussions` Function**: This function uses OpenAI GPT-3 to analyze and generate summaries for the gathered discussions.

    - **`generate_gpt3_summary` Function**: This function sends a prompt to GPT-3 and receives a summary in response.

    - **FastAPI Routes**:
        - **`read_root` Endpoint**: Renders the `index.html` template on a GET request to "/".
        - **`read_item` Endpoint (POST)**: Gathers hot topics, retrieves relevant discussions from Reddit, and analyzes the information using GPT-3. Returns a JSON response with the gathered information.

    - **Application Execution**: The script checks if it is the main module and runs the FastAPI application using the uvicorn server.

## Accessing the Application

Open your web browser and navigate to `http://127.0.0.1:8001/` to access the homepage. The homepage does not require any user input and serves as a starting point for the application.

