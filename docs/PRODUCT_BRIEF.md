# Product Brief – LoL Summoner Analysis Service

## What is this?
A web-based League of Legends analysis service where users can:
- Register summoners
- Collect match histories
- Compute performance scores
- Receive AI-based analysis and team composition recommendations

## Target Users
- LoL players curious about their playstyle and strengths
- Users interested in AI-based performance analysis
- Recruiters reviewing full-stack + AI service prototypes

## Core User Flow
1. Summoner registration (browser)
2. Match data collection (Riot API or mock)
3. Score calculation (roles, performance metrics)
4. AI-based analysis
5. Team composition recommendation

## Non-Goals
- No real-time match tracking
- No ranked matchmaking automation
- No production-grade Riot API scaling

## Tech Stack
- Frontend: React (Vite) + TypeScript + MUI
- Backend: FastAPI + SQLAlchemy
- AI: MockAIProvider (replaceable)

## Constraints
- Riot Dev Key usage
- Personal/portfolio-level infra
- Single-repo, mixed frontend/backend structure
