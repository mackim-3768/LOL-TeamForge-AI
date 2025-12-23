# Weekly Feature Planning - 2025-W10

## 1. Discovery (Ideas)

### 1. Visual Role Performance (Radar Chart)
- **Applies to**: Summoner Detail Page (Frontend).
- **Problem**: Users are presented with a table of numbers for 5 roles, which is hard to quickly digest and compare.
- **Why it matters**: A radar chart provides an instant visual profile of a player (e.g., "All-rounder" vs "One-trick"). It significantly enhances the visual appeal of the portfolio.

### 2. Match History Transparency List
- **Applies to**: Summoner Detail Page (Frontend/Backend).
- **Problem**: Users see aggregated scores but cannot verify the source matches, leading to lack of trust in the data.
- **Why it matters**: Improves transparency and allows users to debug why their score is low (e.g., "Oh, that game I played support Teemo counted").

### 3. Duo Synergy Calculator
- **Applies to**: New "Tools" section or Team Builder.
- **Problem**: Players often queue in pairs but don't know if their playstyles clash (e.g., two passive players in bot lane).
- **Why it matters**: Expands the analysis beyond individual performance to team dynamics, a key differentiator.

### 4. "Playstyle Tags" System
- **Applies to**: Summoner Profile Header.
- **Problem**: Numeric scores (Win Rate, KDA) don't describe *how* someone plays (e.g., "Farmer", "Aggressive", "Visionary").
- **Why it matters**: Adds qualitative descriptors that make the analysis feel more "human" and insightful.

### 5. AI Analyst Persona Selector
- **Applies to**: Analysis Request.
- **Problem**: The default AI analysis can feel generic or repetitive.
- **Why it matters**: Allowing users to choose a persona (e.g., "Roast Master", "Pro Coach", "Encouraging") makes the feature more fun and engaging, showcasing prompt engineering skills.

## 2. Triage

- **Selected Feature**: **Visual Role Performance (Radar Chart)**
- **Reasoning**:
  - **Portfolio Value**: High. A radar chart is visually striking and makes for great screenshots.
  - **Feasibility**: High. The backend already provides normalized 0-100 scores for all roles. This is purely a frontend visualization task.
  - **User Value**: Immediate clarity on player versatility.

- **Why others were not selected**:
  - *Match History*: Essential but visually "boring" compared to a chart. Good candidate for next cycle.
  - *Duo Synergy*: Requires new backend logic and possibly more complex queries.
  - *Tags*: Needs a well-defined logic set to avoid being random.
  - *AI Persona*: Nice to have, but the visual chart improves the core "at-a-glance" analysis better.

## 3. Spec Draft: Visual Role Performance (Radar Chart)

### Feature Name
Visual Role Performance (Radar Chart)

### Problem Statement
The current "Summoner Detail" page displays performance scores in a list/table format. This makes it difficult for users to instantly understand a player's role versatility or focus (e.g., "Is this player a Jungle main or a fill player?").

### MVP Scope
- Install a charting library (e.g., `recharts` or `react-chartjs-2`).
- Create a `RoleRadarChart` component.
- Integrate this component into the `SummonerDetail` page above the scores list.
- Map the existing API response (`/summoners/{name}/scores`) to the chart data format.
- Axes: TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY.
- Data Point: `score` (0-100).

### Optional Scope (Nice to have)
- Overlay a "Class Average" shape for comparison (requires backend stats).
- Tooltips showing the exact score on hover.

### Acceptance Criteria
1. The Summoner Detail page displays a Radar Chart.
2. The chart has 5 axes corresponding to the 5 LoL roles.
3. The shape correctly reflects the `score` values from the API.
4. If a role has no data (score 0/missing), it is plotted as 0.
5. The chart is responsive and fits within the UI layout.

## 4. Backlog Draft

### Title
Feature: Add Role Performance Radar Chart to Summoner Detail

### Tasks
1. **[FE] Install Charting Library**
   - Research and install `recharts` (recommended for React) or `chart.js`.
2. **[FE] Create RoleRadarChart Component**
   - Implement a reusable component that accepts `scores` as props.
   - Configure axes and scaling (0-100).
3. **[FE] Integrate into SummonerDetail**
   - Place the chart component in the layout (likely top section).
   - Pass data from the `get_summoner_scores` API call.
4. **[FE] Styling & Polish**
   - Ensure colors match the app theme (MUI).
   - Add tooltips/legend if necessary.

## 5. Docs / Notes

### README Updates
- Add a screenshot of the new Radar Chart to the "Features" section.
- Update "Tech Stack" if a significant new library (like Recharts) is added.

### Questions for Next Cycle
1. Should we persist the "Match History" details in the DB for the Transparency feature? (Currently checking DB schema is needed).
2. Can we implement a simple "Compare" overlay on the radar chart for two players?
3. How do we handle "Fill" players or roles with very low sample size in the scoring algorithm?
