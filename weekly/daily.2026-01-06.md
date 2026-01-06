# Daily Idea Log (2026-01-06)

## 1. Discovery (Ideas)

### 1. 매치 상세 AI 코칭 (Match Detail AI Coaching)
- **적용 위치**: `SummonerDetail` 페이지 내 매치 상세(Match Detail) 다이얼로그
- **해결하는 문제**: 사용자가 단순히 KDA나 딜량 수치만 보고는 해당 게임의 전략적 승패 요인이나 구체적인 개선점을 파악하기 어려움.
- **중요한 이유**: 수치 데이터(Data)를 인사이트(Insight)로 변환해주는 AI의 핵심 가치를 보여줄 수 있음. 포트폴리오 관점에서 매력적인 기능.

### 2. 팀 빌더 역할 공백 경고 (Team Builder Role Gap Alert)
- **적용 위치**: `TeamBuilder` 페이지
- **해결하는 문제**: 팀 구성 시 AP/AD 밸런스나 탱커 부재 등 조합상의 약점을 사용자가 인지하지 못하는 경우가 있음.
- **중요한 이유**: 팀 구성 추천의 신뢰도를 높이고, 사용자에게 구체적인 가이드를 제공함.

### 3. 최근 퍼포먼스 히트맵 (Recent Performance Heatmap)
- **적용 위치**: `SummonerDetail` 페이지 상단
- **해결하는 문제**: 텍스트 형태의 전적 리스트만으로는 최근 플레이 빈도와 승률 흐름을 한눈에 파악하기 어려움.
- **중요한 이유**: GitHub Contribution 그래프처럼 시각적으로 익숙하고 직관적인 UI로 사용자 경험을 개선함.

### 4. 챔피언 숙련도 뱃지 시스템 (Champion Mastery Badges)
- **적용 위치**: `SummonerDetail` 및 매치 리스트
- **해결하는 문제**: 해당 소환사가 특정 챔피언을 얼마나 깊이 있게 플레이했는지(장인 여부)를 식별하기 어려움.
- **중요한 이유**: 단순 승률 외에 '경험치'라는 척도를 제공하여 분석의 깊이를 더함.

### 5. 듀오 파트너 찾기 (Duo Partner Finder)
- **적용 위치**: `DuoSynergyTool` 또는 신규 페이지
- **해결하는 문제**: "내가 야스오를 하는데 누구랑 해야 할까?"라는 역방향 질문에 대한 답을 찾기 어려움.
- **중요한 이유**: 기존 `duo_synergy.py` 로직을 재활용하여 새로운 가치를 창출할 수 있음.

## 2. Triage

- **Top 1 Feature**: **매치 상세 AI 코칭 (Match Detail AI Coaching)**
- **Selection Reason**:
    - **Impact**: 사용자가 가장 궁금해하는 "내가 왜 졌지/이겼지?"에 대한 직접적인 답을 줄 수 있음.
    - **Feasibility**: 이미 존재하는 `MatchDetail` 데이터와 AI 모듈 구조를 활용하므로 구현 리스크가 적음.
    - **Portfolio Value**: "AI가 개별 게임을 분석해준다"는 시나리오는 매우 강력한 포트폴리오 소구점임.
- **Why others were not selected**:
    - 팀 빌더 개선(2번)이나 듀오 파트너(5번)는 훌륭하지만, 현재 `SummonerDetail` 페이지의 완성도를 높이는 것이 사용자 유입 관점에서 우선순위가 높음.
    - 히트맵(3번)은 데이터가 많이 쌓여야 의미가 있어 Mock 데이터 위주인 현재 환경에서는 효과가 제한적일 수 있음.

## 3. Spec Draft (Top 1 only)

### Feature Name
매치 상세 AI 코칭 (Match Detail AI Coaching)

### Problem Statement
사용자는 매치 기록에서 수치(KDA, 골드 등)만 확인할 수 있어, 해당 게임의 결정적인 승패 요인이나 자신의 플레이에 대한 피드백을 얻기 어렵습니다.

### MVP Scope
- **Backend**:
    - `AIProvider` 인터페이스에 `analyze_match_detail(match_data)` 메서드 추가.
    - `MockAIProvider` 및 `OpenAIProvider` 구현.
    - `/ai/analyze-match` 엔드포인트 생성 (POST).
- **Frontend**:
    - `MatchDetail` 다이얼로그 하단에 "AI 코칭 분석" 섹션 추가.
    - "분석 요청" 버튼 및 로딩/에러 UI 구현.
    - 분석 결과(Markdown 텍스트) 표시 컴포넌트 연동.

### Optional Scope (Not for MVP)
- 특정 시점(15분)에서의 골드 차이 등 시계열 데이터 분석 포함.
- 상대 라이너와의 직접 비교 분석.

### Acceptance Criteria
1. `SummonerDetail`에서 매치 클릭 시 뜨는 다이얼로그에 "AI 분석" 버튼이 보여야 한다.
2. 버튼 클릭 시 Backend API를 호출하고 로딩 스피너가 돌아야 한다.
3. API 응답 성공 시, 다이얼로그 내에 분석 텍스트가 Markdown 형태로 렌더링되어야 한다.
4. `MockAIProvider` 환경에서도 더미 분석 텍스트가 정상적으로 표시되어야 한다.

## 4. Backlog Draft

### GitHub Issue Title
[Daily][2026-01-06] 매치 상세 AI 코칭 기능 구현

### Task Breakdown
- [ ] Backend: `AIProvider.analyze_match_detail` 추상 메서드 및 구현체(Mock/OpenAI) 작성
- [ ] Backend: `POST /ai/analyze-match` API 엔드포인트 구현 및 테스트
- [ ] Frontend: `MatchDetail` 다이얼로그 UI 수정 (분석 버튼 및 결과 표시 영역 추가)
- [ ] Frontend: `api.ts` 업데이트 및 상태 관리 구현

## 5. Docs / Notes

### Suggested README Update
- **Section**: Features
- **Message**: "AI Match Coaching: Get detailed insights on specific matches powered by AI analysis."

### Questions for Next Cycle
1. 매치 분석 시 토큰 사용량을 줄이기 위해 어떤 데이터만 선별해서 프롬프트에 넣어야 할까?
2. 분석 결과를 DB에 캐싱하여 중복 호출을 막아야 할까? (MVP 이후 고려)
3. 사용자가 분석 결과에 대해 "유용함/유용하지 않음" 피드백을 줄 수 있게 해야 할까?
