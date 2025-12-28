# Daily Idea Log: 2025-W10-day1

## 1. Discovery (Ideas)

1. **점수 상세 분석 툴팁 (Frontend)**
   - **위치:** 소환사 상세 페이지 (Summoner Detail) - 종합 점수 표시 영역
   - **문제:** 사용자는 최종 점수(예: 85점)만 확인 가능하며, 어떤 요소(KDA, CS, 시야 등)가 점수에 긍정적/부정적 영향을 미쳤는지 알 수 없음.
   - **가치:** 분석의 **설명력(Explainability)**을 강화하여 사용자의 신뢰도를 높임. 포트폴리오 관점에서 데이터 시각화 능력 어필 가능.
   - 적용 여부: Status: TODO

2. **최근 20게임 승률/KDA 트렌드 그래프 (Frontend)**
   - **위치:** 소환사 상세 페이지
   - **문제:** 텍스트 기반의 매치 리스트로는 최근 실력의 상승/하락세를 파악하기 어려움.
   - **가치:** **직관적인 UX** 제공 및 시계열 데이터 시각화 구현 역량 증명.
   - 적용 여부: Status: TODO

3. **챔피언 숙련도 기반 AI 추천 필터링 (Backend/AI)**
   - **위치:** AI 분석 및 팀 추천 로직
   - **문제:** AI가 사용자가 전혀 플레이해본 적 없는 챔피언을 추천하는 경우 실용성이 떨어짐.
   - **가치:** 추천 시스템의 **개인화** 수준 향상. MockAIProvider 환경에서도 로직 검증 가능.
   - 적용 여부: Status: TODO

4. **티어 평균 대비 내 스탯 비교 (Backend)**
   - **위치:** 소환사 상세 페이지 - 스탯 분석 섹션
   - **문제:** "CS 6.5개"가 좋은 수치인지 나쁜 수치인지 기준점이 모호함.
   - **가치:** 데이터에 **맥락(Context)**을 부여하여 분석의 깊이를 더함.
   - 적용 여부: Status: TODO

5. **API 요청 상태 및 재시도 UI (UX/Infra)**
   - **위치:** 소환사 등록/갱신 화면
   - **문제:** Riot API 호출 실패 시 사용자는 원인을 모르고 마냥 기다리거나 이탈함.
   - **가치:** 예외 처리를 통한 **사용자 경험(UX)** 보호 및 시스템 견고성 확보.
   - 적용 여부: Status: TODO

## 2. Triage

- **Top 1 Feature:** **점수 상세 분석 툴팁**
- **선정 이유 (Selection Reasoning):**
  - **Explainability (설명력):** 이 프로젝트의 핵심 가치인 '분석'을 가장 직관적으로 강화하는 기능입니다.
  - **구현 용이성 (Feasibility):** 기존 백엔드 점수 계산 로직에서 세부 항목만 노출하면 되므로, 큰 리팩토링 없이 MVP 구현이 가능합니다.
  - **ICE Score:** Impact(High) / Confidence(High) / Ease(High)
- **미선정 이유:**
  - 트렌드 그래프: 차트 라이브러리 도입 등 프론트엔드 작업량이 상대적으로 많음.
  - 챔피언 숙련도/티어 비교: 추가 데이터 수집이나 기준 데이터(Baseline) 구축이 선행되어야 함.

## 3. Spec Draft (Top 1 only)

### Feature: 점수 상세 분석 툴팁 (Score Breakdown Tooltips)

**Problem Statement:**
사용자는 소환사의 종합 점수가 어떻게 산출되었는지 알 수 없어, 분석 결과에 대한 구체적인 피드백을 얻기 어렵습니다.

**MVP Scope:**
1. 백엔드: 점수 계산 API 응답에 `sub_scores` (예: `combat`, `farming`, `vision`, `objective`) 필드 추가.
2. 프론트엔드: 종합 점수에 마우스 오버(Hover) 시, 각 세부 항목의 점수를 보여주는 MUI Tooltip 구현.

**Optional Scope:**
- 각 항목별 간단한 코멘트 (예: "CS 수급이 평균 이상입니다") 표시.
- 방사형 차트(Radar Chart)로 시각화.

**Acceptance Criteria:**
- [ ] `/summoner/{name}` API 응답에 세부 점수 항목이 포함되어야 한다.
- [ ] 소환사 상세 페이지의 점수 배지에 마우스를 올리면 툴팁이 나타나야 한다.
- [ ] 툴팁 내에 전투(Combat), 성장(Farming), 시야(Vision) 등의 세부 점수가 표시되어야 한다.

## 4. Backlog Draft

### GitHub Issue Title
`[Daily][2025-W10-day1] Implement Score Breakdown Tooltips for Summoner Analysis`

### Task Breakdown
1. **[Backend]** `calculate_score` 함수 수정하여 세부 점수 항목 반환하도록 DTO 업데이트
2. **[Frontend]** `SummonerScoreCard` 컴포넌트 내 MUI Tooltip 추가
3. **[Frontend]** API 응답 데이터와 툴팁 UI 연동 및 스타일링

## 5. Docs / Notes

### Suggested README Update
- `Features` 섹션에 "Detailed Score Analysis (Combat/Farming/Vision breakdown)" 항목 추가.

### Questions for Next Cycle
1. 현재 점수 계산 로직(`backend/core_api/logic.py` 혹은 유사 경로)이 세부 항목별로 분리되어 있는가?
2. MUI Tooltip 외에 모바일 환경에서는 어떻게 보여줄 것인가? (클릭 시 팝업 등 고려)
3. MockAIProvider가 세부 점수에 대한 텍스트 분석도 생성해 줄 수 있는가?
