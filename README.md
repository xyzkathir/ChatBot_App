# Mashreq Banking Assistant

A simple banking customer service chatbot built with:
- Frontend: HTML, CSS, JavaScript
- Backend: FastAPI
- LLM: Groq with the `openai/gpt-oss-20b` model
- Server: Uvicorn

## Project structure

- `main.py` - FastAPI backend
- `static/index.html` - frontend page
- `static/style.css` - styling
- `static/app.js` - chat UI logic
- `.env` - environment variables for the API key and model
- `requirements.txt` - Python dependencies
- `run_app.bat` - Windows shortcut to run the app

## Setup

1. Open a terminal in the project folder.
2. Create a Python 3.11 environment:

```powershell
py -3.11 -m venv .venv
```

3. Activate the environment:

```powershell
.\.venv\Scripts\activate
```

4. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

5. Make sure your `.env` file contains the Groq API key and model:

```env
GROK_API_KEY=your_api_key_here
GROK_MODEL=openai/gpt-oss-20b
GROK_URL=https://api.groq.com/openai/v1/chat/completions
```

## Run the app

### Option 1: using the batch file

```powershell
./run_app.bat
```

### Option 2: directly

```powershell
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open:

```text
http://127.0.0.1:8000
```

## Notes

This chatbot is designed for simple banking support questions and does not access real account data. It should be used as a customer service assistant and should route sensitive tasks to verified bank channels.
