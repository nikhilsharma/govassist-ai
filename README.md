# GovAssist AI

A hackathon-ready Flask application that helps government officers triage operational issues using a local JSON knowledge base and the OpenAI Responses API.

## Features

- Modern, responsive officer workspace
- Structured analysis: category, summary, stakeholder, verification steps, suggested action, and draft reply
- Local `data/knowledge_base.json` context for grounded results
- SQLite audit trail of submitted issues and analyses
- Graceful demo fallback when `OPENAI_API_KEY` is not configured

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your OpenAI API key.
4. Run: `python app.py`
5. Visit `http://127.0.0.1:5000`

## Project layout

```text
app.py                 Flask application factory and routes
config.py              Environment-based configuration
services/              AI analysis and knowledge-base services
repositories/          SQLite persistence
data/                  Local JSON knowledge base
templates/             HTML templates
static/                CSS and browser JavaScript
```

## Notes

The default model can be changed through `OPENAI_MODEL`. The generated content is a decision-support draft and should be reviewed by an authorized officer before it is issued.
