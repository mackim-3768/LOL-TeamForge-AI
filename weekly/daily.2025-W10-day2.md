# Daily Idea Log: 2025-W10-day2

## 1. Discovery (Ideas)

1. **플레이 스타일 방사형 차트 (Frontend)**
   - **위치:** 소환사 상세 페이지 - 종합 점수 하단
   - **문제:** 단순한 텍스트나 숫자 점수만으로는 플레이어의 강점(전투 지향 vs 운영 지향)을 한눈에 파악하기 어려움.
   - **가치:** **데이터 시각화(Data Visualization)**를 통해 정보를 직관적으로 전달하며, 포트폴리오의 시각적 완성도를 크게 높임.
   - 적용 여부: Status: TODO

2. **모스트 챔피언 요약 섹션 (Frontend/Backend)**
   - **위치:** 소환사 상세 페이지 상단
   - **문제:** 최근 20게임 리스트만 나열되어 있어, 이 플레이어가 주로 무엇을 하는 사람인지(메인 챔피언/포지션) 즉시 알기 어려움.
   - **가치:** 핵심 정보를 요약하여 **사용자 인지 부하(Cognitive Load)**를 줄여줌.
   - 적용 여부: Status: TODO

3. **매치 기록 상세 펼치기 기능 (Frontend)**
   - **위치:** 매치 리스트 아이템
   - **문제:** 현재 리스트에는 KDA만 표시되나, 사용자는 구체적인 아이템 빌드나 룬 선택 등 **근거 데이터**를 보고 싶어 함.
   - **가치:** 페이지 이동 없이 깊이 있는 정보를 제공하여 **탐색 경험(Navigation Experience)** 개선.
   - 적용 여부: Status: DONE

4. **AI 분석 페르소나(코치/분석가) 선택 (AI/Backend)**
   - **위치:** AI 분석 요청 전/설정 단계
   - **문제:** AI의 분석 톤이 일률적이어서 재미가 없고 개인화된 느낌이 부족함. ("칭찬 위주" vs "팩트 폭력")
   - **가치:** **프롬프트 엔지니어링** 역량을 보여줄 수 있으며, 사용자에게 선택권을 주어 참여도를 높임.
   - 적용 여부: Status: TODO

5. **티어/랭크 정보 연동 및 표시 (Backend/Infra)**
   - **위치:** 소환사 프로필 헤더
   - **문제:** 자체 점수(Score)만으로는 객관적인 실력 척도(실제 랭크)와의 비교가 불가능함.
   - **가치:** 데이터의 **신뢰성(Credibility)** 확보 및 Riot API 활용 범위 확장.
   - 적용 여부: Status: TODO

## 2. Triage

- **Top 1 Feature:** **플레이 스타일 방사형 차트 (Playstyle Radar Chart)**
- **선정 이유 (Selection Reasoning):**
  - **Portfolio Value (포트폴리오 가치):** 텍스트 위주의 UI에 시각적 임팩트를 주는 가장 효과적인 기능입니다. 방사형 차트는 게임 분석 서비스의 표준적인 UX이기도 합니다.
  - **Continuity (연속성):** Day 1에서 제안된 '세부 점수(Score Breakdown)' 데이터를 활용하여 시각화하는 자연스러운 확장 기능입니다.
  - **ICE Score:** Impact(High) / Confidence(High) / Ease(Medium - 차트 라이브러리 학습 필요)
- **미선정 이유:**
  - 모스트 챔피언/매치 상세: 유용하지만 시각적 임팩트가 차트보다 약함.
  - AI 페르소나: 백엔드/AI 프롬프트 작업이 주가 되며, 현재 MockAI 환경에서는 효과가 제한적일 수 있음.

## 3. Spec Draft (Top 1 only)

### Feature: 플레이 스타일 방사형 차트 (Playstyle Radar Chart)

**Problem Statement:**
숫자로 된 세부 점수는 직관적이지 않아, 사용자가 자신의 플레이 스타일(공격적/방어적/운영형 등)을 패턴으로 인식하기 어렵습니다.

**MVP Scope:**
1. 프론트엔드: 차트 라이브러리(예: `recharts` 또는 `chart.js`) 도입.
2. 프론트엔드: 5가지 축(전투, 성장, 시야, 생존, 오브젝트)을 가진 방사형 차트(Radar Chart) 구현.
3. 데이터 연동: 백엔드에서 제공하는 정규화된(0~100) 세부 점수를 차트에 매핑.

**Optional Scope:**
- 툴팁 추가 (마우스 오버 시 정확한 수치 표시).
- 애니메이션 효과 (로딩 시 차트가 그려지는 모션).

**Acceptance Criteria:**
- [ ] 소환사 상세 페이지에 오각형 형태의 방사형 차트가 렌더링되어야 한다.
- [ ] 5개의 축(Combat, Farming, Vision, Survival, Objective)이 모두 표시되어야 한다.
- [ ] 데이터가 없는 경우(0점)에도 차트가 깨지지 않고 빈 형태로 표시되어야 한다.
- [ ] 모바일 화면에서도 차트가 영역을 벗어나지 않고 반응형으로 표시되어야 한다.

## 4. Backlog Draft

### GitHub Issue Title
`[Daily][2025-W10-day2] Implement Playstyle Radar Chart for Summoner Analysis`

### Task Breakdown
1. **[Frontend]** `recharts` 라이브러리 설치 및 설정 (`npm install recharts`)
2. **[Backend]** `calculate_score` 로직에서 각 세부 점수를 100점 만점 기준으로 정규화(Normalize)하여 반환하도록 수정
3. **[Frontend]** `RadarChartComponent` 생성 및 데이터 바인딩
4. **[Frontend]** 차트 색상 및 스타일 테마(MUI 연동) 적용

## 5. Docs / Notes

### Suggested README Update
- `Tech Stack` 섹션에 `Recharts` (또는 선정된 라이브러리) 추가.
- `Screenshots` 섹션에 차트가 포함된 분석 페이지 예시 추가 예정.

### Questions for Next Cycle
1. `Recharts`가 React 19 및 Vite 환경에서 호환성 문제가 없는가? (없다면 `Chart.js` 고려)
2. 5각형 스탯의 기준(만점)을 어떻게 정할 것인가? (예: 챌린저 평균을 100으로 할 것인가, 절대 평가인가?)
3. 다크 모드 지원 시 차트의 그리드/축 색상은 어떻게 처리할 것인가?
