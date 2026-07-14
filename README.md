# GovAssist AI

GovAssist AI is an AI-assisted decision support prototype built during the OpenAI Codex Hackathon.

The application helps government officers analyse operational issues by retrieving the most relevant operational playbook from a structured knowledge base and presenting verification steps, suggested actions, and a draft official reply.

The current prototype has been developed using MPLADS operational workflows but the architecture is generic and can be adapted for other government departments by replacing the knowledge base.

---

## Features

- AI-assisted operational issue analysis
- Local operational knowledge base (`knowledge_base.json`)
- Retrieval of the most relevant operational playbook
- Structured operational guidance including:
  - Issue Category
  - Relevant Stakeholder
  - Summary
  - Verification Steps
  - Suggested Action
  - Draft Official Reply
- Displays the matched operational playbook used for analysis
- SQLite audit trail of analysed issues
- Runs in local demo mode without an OpenAI API key
- Automatically switches to OpenAI Responses API when an API key is configured

---

## Technology Stack

- Python
- Flask
- OpenAI Responses API
- SQLite
- HTML
- CSS
- JavaScript

---

## Project Structure

```text
app.py                     Flask application
config.py                  Environment configuration

data/
    knowledge_base.json    Operational playbooks

services/
    analysis_service.py
    knowledge_base_service.py

repositories/
    issue_repository.py

templates/
    index.html

static/
    css/
    js/
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/nikhilsharma/govassist-ai.git
cd govassist-ai
```

### 2. Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Configure OpenAI

Copy

```
.env.example
```

to

```
.env
```

and add

```
OPENAI_API_KEY=your_api_key_here
```

If no API key is configured, the application automatically runs in demo mode using the local knowledge base.

### 5. Run the application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

## Knowledge Base

Operational procedures are maintained in

```
data/knowledge_base.json
```

Each operational playbook contains:

- Title
- Category
- Keywords
- Stakeholder
- Verification Steps
- Suggested Action
- Draft Official Reply

Adding new operational issues only requires adding a new playbook to the knowledge base. No application code changes are required.

---

## Current Prototype

The current knowledge base includes operational workflows such as:

- Vendor Validation
- PFMS / Payments
- LGD Mapping
- Portal Access
- MPLADS Administration

The same architecture can be adapted for other government departments by replacing the operational playbooks.

---

## Notes

- AI-generated responses are intended as decision-support drafts.
- Officers should review all generated outputs before official use.
- The OpenAI model can be configured through `OPENAI_MODEL`.