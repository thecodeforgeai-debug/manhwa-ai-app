# Manhwa Intel

AI-powered manhwa recommendation platform with real-time trending data and semantic search.

![Manhwa Intel Screenshot](./screenshot.png)


## Live Demo
🔗 [Coming Soon](#)

## What It Does
- **Trending District** — Daily updated rankings pulled from Anilist & MangaDex APIs
- **AI-Powered Recommendations** — "Neural Scan" uses Claude API to match users with manhwa based on preferences
- **Smart Filtering** — Filter by genres (Action, Fantasy, Romance, etc.) and tropes (System, Reincarnation, Dungeon Crawl, etc.)
- **Search** — Fast search across 400+ titles

## Tech Stack
**Frontend**
- Next.js (App Router)
- TypeScript
- Tailwind CSS
- Custom cyberpunk UI system

**Backend**
- FastAPI (Python)
- SQLite database
- Claude API (Anthropic) for AI recommendations
- Anilist & MangaDex API integrations

## Technical Highlights
- CORS configuration for frontend/backend communication
- Rate limiting & input validation
- API proxy pattern to protect external API keys
- Error handling with loading states
- Responsive design

## Why I Built This
To demonstrate full-stack development with:
- Real third-party API integrations
- AI/LLM integration in a practical use case
- Production-style architecture (separate frontend/backend)
- Clean, themed UI design

## Run Locally
```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Contact
Open to freelance work — [DM me](https://github.com/thecodeforgeai-debug)
