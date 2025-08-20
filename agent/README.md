# Research React Agent

This directory now includes a Farcaster agent (`farcaster_agent.py`) that demonstrates how to use LangGraph with tools for the Neynar Farcaster API. It exposes utilities to fetch user profiles and feeds, manage signers, and post casts directly from the agent.

## Running the HTTP service

To make the agent accessible from the frontend, a small FastAPI server is provided in `server.py`.

```bash
pip install -r requirements.txt
python server.py  # starts on http://localhost:8000
```

Send a POST request with a user message:

```bash
curl -X POST http://localhost:8000/farcaster -H 'Content-Type: application/json' -d '{"message": "Hello"}'
```

The server will run the graph and return the agent's response as JSON.
