# PitchIQ — AI Investor Memo Generator

> Transform any startup idea into a professional investor memo in under 5 minutes using multi-agent AI.

---

## 🚀 What is PitchIQ?

PitchIQ is an AI-powered platform that turns startup descriptions into investor-ready memos. Describe your startup in plain English, and our multi-agent system handles the rest—market research, competitive analysis, funding intelligence, and professional memo writing.

---

## ✨ Features

- **5 Specialized AI Agents** – Intake, Market Research, Funding, VC Memo, and Quality Review
- **Real-Time Research** – MCP tools for live web search and funding data
- **Production Database** – PostgreSQL with connection pooling
- **Modern Frontend** – Next.js 15 with dark theme and real-time progress tracking
- **Security-First** – Input validation, injection detection, rate limiting
- **Docker Support** – One-command deployment with Docker Compose

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Backend** | Python 3.12, FastAPI, Google ADK, Gemini 2.5 Flash, PostgreSQL, SQLAlchemy |
| **Frontend** | Next.js 15, TypeScript, Tailwind CSS, Framer Motion |
| **Infrastructure** | Docker, Docker Compose |

---

## 📁 Project Structure

```
PitchIQ/
├── backend/
│   ├── agents/          # 5 specialist agents + orchestrator
│   ├── mcp_server/      # MCP tools (web_search, funding_lookup)
│   ├── routers/         # API endpoints
│   ├── security/        # Security layer
│   ├── models.py        # Database models
│   └── main.py          # FastAPI entry point
├── frontend/
│   ├── src/app/         # Next.js pages
│   └── src/components/  # UI components
├── docker-compose.yml
└── .env.example
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- Docker (optional)

### Option 1 — Run with Docker (Recommended)

```bash
# Clone and setup
git clone https://github.com/yourusername/PitchIQ.git
cd PitchIQ
cp .env.example .env

# Add your API key to .env
# GOOGLE_API_KEY=your_key_here

# Build and run
docker-compose up -d --build

# Access
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2 — Run Locally

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## 🔑 Environment Variables

```env
GOOGLE_API_KEY=your_google_api_key_here
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql+asyncpg://pitchiq:password@localhost:5432/pitchiq
```

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## 📖 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/generate` | Submit startup description |
| `GET /api/status/{job_id}` | Check generation progress |
| `GET /api/memo/{job_id}` | Retrieve completed memo |
| `GET /api/mcp/tools` | List available MCP tools |
| `GET /health` | System health check |

---

## 🧪 Testing

```bash
cd backend
pytest tests/ -v
```

---

## 🔮 Future Improvements

- [ ] User authentication (JWT + API keys)
- [ ] PDF memo export
- [ ] Redis caching
- [ ] WebSocket real-time updates
- [ ] CI/CD pipeline

---

## 🙌 Acknowledgments

Built for the **Kaggle Agents Intensive Capstone** using:
- Google ADK (Agent Development Kit)
- Google Gemini 2.5 Flash
- Model Context Protocol (MCP)

---

