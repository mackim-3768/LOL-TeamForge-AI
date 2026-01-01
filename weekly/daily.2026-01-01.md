# Daily Idea Planning - 2026-01-01

## 1. Discovery (Ideas)

### 1. Summoner Performance Radar Chart (Insight Depth / UX)
- **User Flow:** Summoner Detail Page
- **Problem:** 사용자는 단순한 점수(Score)만으로는 자신의 구체적인 강점(시야, 전투, 성장 등)을 파악하기 어렵습니다.
- **Why:** KDA, 골드, 시야 점수 등의 세부 지표를 시각화하여 플레이 스타일을 직관적으로 보여줍니다. 포트폴리오 관점에서 시각적 요소는 매우 중요합니다.

### 2. Recent Match Trend Graph (Insight Depth)
- **User Flow:** Summoner Detail Page
- **Problem:** 최근 20게임 동안 실력이 상승세인지 하락세인지 파악하기 어렵습니다.
- **Why:** 승률이나 KDA의 변화 추이를 선 그래프로 보여주어 사용자의 성장을 시각화합니다.

### 3. AI Analysis "Reasoning Log" (Explainability)
- **User Flow:** AI Analysis Result
- **Problem:** AI가 왜 그런 분석을 했는지, 왜 그런 팀 조합을 추천했는지 "블랙박스"로 느껴질 수 있습니다.
- **Why:** AI 프롬프트의 핵심 요약이나 분석 근거를 "더 보기" 형태로 제공하여 신뢰도를 높이고, 개발 역량(AI 통합 이해도)을 어필할 수 있습니다.

### 4. Champion Pool Scatter Plot (Insight Depth)
- **User Flow:** Summoner Detail Page
- **Problem:** 어떤 챔피언이 승률은 높지만 표본이 적은지(장인 챔프), 많이 하지만 승률이 낮은지(함정 챔프) 한눈에 보기 어렵습니다.
- **Why:** X축(플레이 횟수), Y축(승률)의 산점도로 챔피언 풀을 시각화하여 전략적 선택을 돕습니다.

### 5. Mock Data Generator UI (Developer Experience)
- **User Flow:** Admin Page
- **Problem:** 라이엇 API 키 만료나 제한 상황에서 기능을 테스트하거나 시연하기 어렵습니다.
- **Why:** 버튼 하나로 가상의 전적 데이터를 생성하여 로컬 개발 속도를 높이고, 안정적인 데모 환경을 구축할 수 있습니다.

---

## 2. Triage

### Top 1 Feature: Summoner Performance Radar Chart
- **Selection Reason:**
  - **Impact (High):** 텍스트/표 위주의 현재 UI에 강력한 시각적 요소를 더해 사용자 경험을 크게 개선합니다.
  - **Feasibility (High):** 이미 `recharts`가 설치되어 있고, 백엔드에 필요한 원본 데이터(`MatchPerformance`)가 대부분 존재합니다.
  - **Portfolio Value:** 데이터 시각화 능력은 분석 서비스 포트폴리오의 핵심 역량 중 하나입니다.

### Rejected Ideas Reason
- **Recent Match Trend Graph:** Radar Chart가 "종합적인 스타일"을 보여주는 데 더 적합한 MVP 시각화라고 판단했습니다. 추후 추가 가능.
- **AI Analysis Reasoning Log:** 매우 좋은 아이디어이나, 현재 AI 응답 구조를 변경해야 할 수도 있어 공수가 조금 더 큽니다.
- **Champion Pool Scatter Plot:** 데이터가 충분히 쌓여야 의미가 있으므로, 초기 단계에서는 Radar Chart가 더 유용합니다.
- **Mock Data Generator:** 유용하지만 사용자 경험보다는 개발자 도구에 가까워 우선순위에서 밀렸습니다.

---

## 3. Spec Draft

### Feature Name
Summoner Performance Radar Chart (육각형 스탯 그래프)

### Problem Statement
사용자는 자신의 플레이 스타일(전투 지향형인지, 운영 지향형인지 등)을 숫자로만 확인해야 해서 직관적인 이해가 어렵습니다.

### MVP Scope
1. **Backend:**
   - `ScoreResponse`에 `avg_damage`, `avg_cs` 필드를 추가합니다.
   - 각 지표(KDA, Gold, Vision, Damage, CS)의 평균값을 계산하여 반환합니다.
2. **Frontend:**
   - `SummonerDetail` 페이지에 `RadarChart` 컴포넌트를 추가합니다.
   - 각 축은 0~100점 스케일로 정규화하거나, 원본 값을 표시하되 축의 범위를 적절히 설정합니다. (MVP는 단순 원본 값 혹은 백엔드에서 정규화된 점수 사용 고려)
   - *Note:* 현재 백엔드 로직에 이미 `OP_SCORE` 계산을 위한 가중치/기준값이 있으므로 이를 활용하거나, 단순히 평균값을 보여주고 프론트엔드에서 `domain`을 설정합니다.

### Optional Scope
- 각 지표를 티어 평균과 비교하여 백분위로 표시 (데이터 부족으로 제외)
- 차트 툴팁에 상세 수치 표시

### Acceptance Criteria
- [ ] API `/summoners/{name}/scores` 응답에 `avg_damage`, `avg_cs`가 포함되어야 한다.
- [ ] 소환사 상세 페이지에 5각형(또는 그 이상)의 레이더 차트가 렌더링되어야 한다.
- [ ] 차트의 각 축은 KDA, 승률, 시야, 골드, 데미지(또는 CS)를 나타내야 한다.
- [ ] 데이터가 없는 경우 차트가 비어있거나 적절한 안내 메시지가 나와야 한다.

---

## 4. Backlog Draft

### Suggested GitHub Issue Title
`[Daily][2026-01-01] Implement Summoner Performance Radar Chart`

### Task Breakdown
1. **Backend**
   - [ ] `backend/core_api/main.py`: `ScoreResponse` 모델에 `avg_damage`, `avg_cs` 필드 추가.
   - [ ] `backend/core_api/main.py`: `_compute_role_scores_for_summoner` 함수에서 데미지와 CS 평균 계산 로직 추가.
2. **Frontend**
   - [ ] `frontend/src/components/PerformanceRadarChart.tsx`: Recharts를 이용한 레이더 차트 컴포넌트 구현.
   - [ ] `frontend/src/pages/SummonerDetail.tsx`: API 응답 데이터를 차트 컴포넌트에 연결 및 배치.

---

## 5. Docs / Notes

### Suggested README Update
- **Features** 섹션에 "Summoner Playstyle Visualization (Radar Chart)" 항목 추가.

### Questions for Next Cycle
1. 레이더 차트의 각 축 스케일이 서로 다른데(예: KDA는 0~10, 골드는 10000~20000), 이를 프론트엔드에서 정규화해서 보여줄지 백엔드에서 0~100 점수로 환산해서 줄지 결정 필요. (이번엔 프론트엔드에서 `polarRadius`나 `domain`을 조정하는 방향으로 시도)
2. `MatchPerformance` 테이블에 `total_damage_dealt_to_champions` 데이터가 과거 데이터에도 잘 들어가 있는지 확인 필요.
