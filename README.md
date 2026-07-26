# DevOps AI Assistant

A beginner Docker + AWS + AI DevOps project. Full step-by-step instructions are in
`DevOps_AI_Assistant_Beginner_Guide.docx`. This README is just a quick command reference.

## Local run (no Docker)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here   # Windows (cmd): set GEMINI_API_KEY=your_key_here
python app.py
```

Visit http://localhost:5000

## Local run (Docker)

```bash
docker build -t devops-ai-assistant .
docker run -d -p 5000:5000 -e GEMINI_API_KEY=your_key_here --name ai-assistant devops-ai-assistant
```

## Push to Docker Hub

```bash
docker login
docker tag devops-ai-assistant YOUR_DOCKERHUB_USERNAME/devops-ai-assistant:latest
docker push YOUR_DOCKERHUB_USERNAME/devops-ai-assistant:latest
```

## Files in this project

| File | Purpose |
|---|---|
| `app.py` | Flask app + Gemini AI agent |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container build instructions |
| `.dockerignore` | Files excluded from the Docker image |
| `.gitignore` | Files excluded from Git |
| `.env.example` | Template for your local `GEMINI_API_KEY` |
| `.github/workflows/deploy.yml` | CI/CD pipeline: build → push → deploy to EC2 |

## Required GitHub Actions secrets

Set these under **Settings → Secrets and variables → Actions**:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `EC2_HOST`
- `EC2_SSH_KEY`
- `GEMINI_API_KEY`
