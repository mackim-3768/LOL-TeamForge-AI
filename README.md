# LoL Flex Rank Analyst

## Project Overview
This project is a Microservices-based application to analyze League of Legends Flex Rank performance. It collects data from the Riot Games API, calculates scores per role, and uses AI to provide insights and team composition recommendations.

## Structure
- `frontend/`: React application (Vite + MUI).
- `backend/`: Python backend.
  - `collector/`: Service to poll Riot API and store match data.
  - `core_api/`: FastAPI service for serving data and AI analysis.
  - `shared/`: Shared Database models and configuration.

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+
- Riot Games API Key (Development Key)

### 1. Database & Backend Setup
Navigate to the root directory.

```bash
# Install Python dependencies
pip install -r backend/requirements.txt
```

### 2. Run Services
You can run the services individually or use the provided script (if created).

**Terminal 1: Core API**
```bash
export PYTHONPATH=$PYTHONPATH:.
uvicorn backend.core_api.main:app --reload --port 8000
```

**Terminal 2: Collector Service (Optional for manual testing)**
The collector service runs a scheduler. In a real deployment, it runs independently.
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 -c "from backend.collector.collector_service import CollectorService; CollectorService().start(); import time; time.sleep(10000)"
```
*Note: The Core API triggers the collector manually upon summoner registration for immediate feedback.*

**Terminal 3: Frontend**
```bash
cd frontend
npm install
npm run dev
```

### 3. Usage
1. Open the frontend (usually `http://localhost:5173`).
2. Enter a Summoner Name (e.g., a valid KR summoner if you have a real key, otherwise mocks might be needed for full flow without key).
3. **Important**: Since we don't have a permanent Riot Key in the repo, you must update it via the Admin API or Environment Variable if you want real data.
   - Or, rely on the `MockAIProvider` for the AI parts.
   - For real data collection, ensure `RIOT_API_KEY` is set in `backend/collector/config.py` or via endpoint.

## Development Notes
- The database is `sqlite:///./dev.db` by default.
- AI is currently using `MockAIProvider`. To enable OpenAI, update `backend/core_api/ai_module.py` with a valid key.
