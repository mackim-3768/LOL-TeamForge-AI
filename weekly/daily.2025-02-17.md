# 2025-02-17 아이디어 노트

## 1. Discovery (Ideas)

### 1. 플레이 스타일 태그 상세 설명 (Explainability)
- **적용 위치:** `SummonerDetail` 페이지의 태그 목록 영역
- **문제:** 사용자는 자신이 왜 "라인전 킬러"나 "시야 사령관" 태그를 받았는지 구체적인 이유(수치)를 알 수 없음.
- **중요성:** 분석의 신뢰도를 높이고, 단순 텍스트 나열이 아닌 데이터 기반의 인사이트임을 증명함.

### 2. 매치별 임팩트 스코어 리스트 노출 (UX Clarity)
- **적용 위치:** `SummonerDetail` 페이지의 `Recent Matches` 리스트
- **문제:** 현재 승/패와 KDA만 노출되어, 해당 판에서 사용자가 얼마나 잘했는지 직관적으로 파악하기 어려움 (`op_score`는 상세 모달에만 있음).
- **중요성:** 리스트에서 빠르게 자신의 "캐리 판"과 "범인 판"을 식별할 수 있게 함.

### 3. 역할군별 성과 트렌드 그래프 (Insight Depth)
- **적용 위치:** `SummonerDetail` 페이지 `Role Performance` 레이더 차트 옆
- **문제:** 레이더 차트는 현재 평균만 보여주어, 최근 실력이 상승세인지 하락세인지 알 수 없음.
- **중요성:** 성장의 즐거움을 제공하고, 슬럼프 구간을 시각화하여 동기 부여.

### 4. 듀오 시너지 상세 분석 (Insight Depth)
- **적용 위치:** `DuoSynergyTool` 결과 화면
- **문제:** 현재 시너지 점수만 나오고, 구체적으로 어떤 스타일(예: "초반 공격형" + "후반 지향형")이 잘 맞는지/안 맞는지 설명이 부족함.
- **중요성:** 단순히 "좋다/나쁘다"를 넘어 "어떻게 플레이해야 하는지" 전략적 가이드를 제공.

### 5. AI 페르소나 선택 기능 (UX/Fun)
- **적용 위치:** `SummonerDetail` AI 분석 요청 버튼 근처
- **문제:** AI 분석 톤이 단조로울 수 있음.
- **중요성:** "엄격한 코치", "부드러운 조언자", "데이터 분석가" 등 페르소나를 선택하게 하여 MockAI라도 사용자 경험을 다채롭게 만듦.

---

## 2. Triage

- **Top 1 Feature:** **플레이 스타일 태그 상세 설명 (Tag Explanation Tooltip)**
- **선정 이유:**
  - **Explainability (높음):** 현재 백엔드 로직(`playstyle_tags.py`)은 정교한 가중치와 임계값을 가지고 있으나, UI에서는 이를 전혀 활용하지 못하고 있음. 가장 적은 비용으로 가장 큰 "분석의 깊이"를 보여줄 수 있는 기능.
  - **Feasibility (높음):** 기존 계산 로직에서 중간 값(score)만 리턴해주면 됨.
- **탈락 이유:**
  - **트렌드 그래프:** 데이터 집계 방식 변경이 필요하여 공수가 큼.
  - **듀오 시너지:** 현재 단일 유저 분석 흐름(Core Flow) 개선이 우선.

---

## 3. Spec Draft (Top 1)

### Feature Name
플레이 스타일 태그 근거 시각화 (Playstyle Explainability)

### Problem Statement
사용자는 `SummonerDetail` 페이지에서 자신에게 부여된 태그("시야 사령관" 등)의 근거를 알 수 없어, 분석 결과를 신뢰하거나 개선점을 찾기 어렵다.

### MVP Scope
1. **Backend**:
   - `playstyle_tags.py`의 `evaluate_tags_for_role` 함수가 태그 선정 시 계산된 `score`와 해당 태그의 `threshold`를 함께 반환하도록 수정.
   - DB 스키마(`SummonerPlaystyleTag`)의 JSON 구조에 점수 정보 포함.
2. **Frontend**:
   - `SummonerDetail.tsx`에서 태그에 마우스를 올리면(Hover) `Tooltip`을 표시.
   - Tooltip 내용: 태그 설명(기존 label), 획득 점수 / 기준 점수 (예: 0.85 / 0.75).

### Optional Scope
- 태그 선정에 기여한 주요 지표 상위 2개 표시 (예: "시야 점수 기여도 높음").

### Acceptance Criteria
- [ ] API `/summoner/{name}/playstyle` 응답의 `tags` 배열 내 객체에 `score`, `threshold` 필드가 존재해야 함.
- [ ] 프론트엔드에서 태그 호버 시 툴팁이 즉시 나타나야 함.
- [ ] 툴팁에 "내 점수"와 "기준 점수"가 명확히 표시되어야 함 (예: Score: 0.82 (Cut: 0.7)).

---

## 4. Backlog Draft

### Title
[Daily][2025-02-17] 플레이 스타일 태그 상세 점수 노출 (Explainability)

### Tasks
- [Frontend] `SummonerDetail.tsx`에 MUI `Tooltip` 컴포넌트 적용 및 태그 렌더링 로직 개선
- [Frontend] `api.ts`의 `PlaystyleTagSnapshot` 타입 정의에 `score`, `threshold` 필드 추가
- [Backend] `playstyle_tags.py` 로직 수정: 태그 선정 시 계산된 score를 결과 딕셔너리에 포함
- [Backend] `upsert_playstyle_snapshot` 호출 시 변경된 데이터 구조가 DB에 정상 저장되는지 확인

---

## 5. Docs / Notes

### README Update
- **Section:** Feature List / Analysis
- **Message:** "플레이 스타일 태그 시스템은 단순 통계가 아닌, 15가지 이상의 세부 지표 가중치 합산을 통해 도출되며, UI에서 그 근거 점수를 확인할 수 있습니다."

### Questions & Uncertainties
1. 기존에 저장된 태그 데이터(DB)에는 `score` 필드가 없을 텐데, 마이그레이션이 필요한가? -> MVP에서는 재계산(`recalc`) 버튼을 누르면 갱신되므로 하위 호환성만 체크(Optional chaining)하면 될 듯.
2. 점수가 1.0을 넘는 경우(캡핑)는 어떻게 표현할 것인가? -> 현재 로직상 `min(1.0, ...)` 처리가 되어 있으나 확인 필요.
3. 모바일 환경에서 호버(Tooltip)가 불편할 수 있는데, 클릭 시 다이얼로그로 띄워야 할까? -> 일단 MVP는 PC 기준 툴팁으로 진행.
