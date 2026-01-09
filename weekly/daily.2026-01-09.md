# Daily Idea Log (2026-01-09)

## 1. Discovery (Ideas)

### 1. 팀 빌더 조직력 점수 (Team Cohesion Score)
- **위치**: Team Builder 페이지
- **문제**: 현재 팀 빌더는 AI의 텍스트 추천에만 의존하며, 선택된 팀원들 간의 정량적인 시너지를 알 수 없음.
- **가치**: 기존 구현된 `duo_synergy` 로직을 확장하여, 팀원 간의 평균적인 스타일 합(Fit)을 점수로 보여주어 AI 분석의 신뢰도를 보완함.

### 2. 가상 프로필 비교 (Mock Profile Comparison)
- **위치**: Summoner Detail / Duo Synergy
- **문제**: 듀오 파트너가 없는 솔로 플레이어는 자신의 스타일이 어떤 유형과 잘 맞는지 알기 어려움.
- **가치**: "공격적 정글러", "수비적 서포터" 등 가상의 이상적 프로필과 나를 비교하여, 내가 찾아야 할 파트너 유형을 제시함.

### 3. 매치 히스토리 하이라이트 태그 (Match Highlight Tags)
- **위치**: Summoner Detail > Match List
- **문제**: 매치 리스트가 단순히 승패/KDA만 나열되어, 해당 게임에서의 구체적 기여(캐리 여부 등)를 한눈에 파악하기 힘듦.
- **가치**: OP Score 기반으로 "ACE", "MVP", "Throwing" 등의 태그를 매치마다 부착하여 리스트의 가독성과 재미를 높임.

### 4. 점수 상세 분석 모달 (Detailed Score Breakdown)
- **위치**: Summoner Detail > Role Radar Chart
- **문제**: "Top Score 85"라는 숫자가 어떤 세부 지표(CS, Vision, KDA 등)에 의해 산출되었는지 알 수 없음.
- **가치**: 점수 산정 공식의 투명성을 높이고(Explainability), 유저가 어떤 부분을 개선해야 점수가 오를지 알 수 있게 함.

### 5. 테스트용 모의 데이터 생성기 (Mock Data Generator)
- **위치**: Admin 페이지
- **문제**: 포트폴리오 시연 시 Riot API 키가 없거나 만료된 경우, 풍부한 데이터를 보여주기 위해 DB를 수동 조작해야 함.
- **가치**: 버튼 클릭 한 번으로 특정 소환사에게 가상의 매치 데이터 20개를 생성해주어, 개발 생산성 및 데모 안정성을 확보함 (DX).

---

## 2. Triage

### **Top 1 Feature: 팀 빌더 조직력 점수 (Team Cohesion Score)**

**선정 이유 (Selection Reasoning):**
- **기존 자산 활용 (Feasibility):** 이미 `backend/core_api/duo_synergy.py`에 강력한 시너지 계산 로직이 구현되어 있어, 이를 N명 대상으로 확장하기만 하면 됨.
- **제품 가치 (Value):** 단순히 AI에게 텍스트를 묻는 것을 넘어, 자체 알고리즘을 통해 정량적 근거를 제시함으로써 서비스의 깊이(Depth)를 보여줄 수 있음.
- **설명 가능성 (Explainability):** AI가 "이 팀이 좋습니다"라고 할 때, "평균 시너지 점수 85점"이라는 근거가 뒷받침됨.

**탈락 이유 (Rejection Reasoning):**
- **Idea 2:** 팀 빌더 기능 강화가 우선순위가 더 높다고 판단됨.
- **Idea 3, 5:** UI/UX 개선이나 DX 향상은 좋으나, "핵심 분석 기능"의 임팩트 면에서 Idea 1보다 약함.
- **Idea 4:** 개발자에게는 좋으나, 최종 사용자(End User) 경험과는 무관함.

---

## 3. Spec Draft

### Feature Name: Team Cohesion Score Integration

### Problem Statement
사용자는 Team Builder에서 소환사 5명을 선택했을 때, AI의 주관적(생성형) 분석 외에 객관적인 데이터 기반의 팀 호흡(Synergy)을 확인할 수 없다.

### MVP Scope
1. **Backend**:
   - `TeamCompRequest` 처리 시, 선택된 소환사들 간의 모든 가능한 듀오 조합(최대 10개)에 대해 `Style Synergy`를 계산.
   - 평균 값을 `cohesion_score`(0~100)로 산출하여 응답에 포함.
2. **Frontend**:
   - AI 분석 결과 카드 상단에 "Team Cohesion Score"를 Progress Bar와 함께 표시.
   - 점수에 따라 색상 구분 (예: 80+ 초록, 50- 노랑, 50미만 빨강).

### Acceptance Criteria
- [ ] 2명 이상의 소환사가 선택되었을 때 Cohesion Score가 계산되어야 한다.
- [ ] 선택된 소환사 중 데이터가 없는 경우(등록되지 않음 등), 해당 소환사를 제외하거나 0점으로 처리하되 에러가 나지 않아야 한다.
- [ ] 결과 점수는 0~100 사이의 정수여야 한다.
- [ ] AI 분석 로딩 중에도(또는 완료 시) 점수가 직관적으로 보여야 한다.

---

## 4. Backlog Draft

### Title: [Daily][2026-01-09] Team Builder Cohesion Score Integration

### Tasks
#### Backend
1. `backend/core_api/duo_synergy.py` 리팩토링: `compute_style_synergy` 로직을 독립적으로 호출하기 쉽게 정리 (이미 되어있다면 재확인).
2. `backend/core_api/main.py`: `recommend_team` 엔드포인트 수정.
   - 입력된 소환사 리스트(`summoner_names`)를 순회하며 `Summoner` 객체 로드.
   - `itertools.combinations`를 사용하여 쌍(Pair) 생성.
   - 각 쌍에 대해 스타일 시너지 계산 후 평균 산출.
   - `AnalysisResponse` 모델에 `cohesion_score` 필드 추가 및 반환.

#### Frontend
1. `frontend/src/api.ts`: `AnalysisResponse` 타입 정의 업데이트 (`cohesion_score` 추가).
2. `frontend/src/pages/TeamBuilder.tsx`:
   - 응답받은 `cohesion_score`를 시각화하는 컴포넌트(예: `<LinearProgress>`) 추가.
   - 점수 구간별 색상 및 텍스트("Excellent", "Good", "Bad") 처리.

---

## 5. Docs / Notes

### README Update
- **Features 섹션**: "Team Builder with AI & **Cohesion Metrics**"로 업데이트하여, 단순 AI 래퍼가 아니라 자체 분석 엔진이 있음을 강조.

### Questions to Explore
1. 5인 팀의 경우 "바텀 듀오"의 시너지 가중치를 "탑-미드" 시너지보다 높게 줘야 할까? (MVP 이후 고려)
2. 데이터가 부족한 신규 소환사가 섞여 있을 때 점수 보정은 어떻게 할 것인가? (현재는 0점 처리 가능성 높음)
3. 5명이 아닌 2~4명 선택 시에도 부분 팀 시너지를 보여주는 것이 UX적으로 자연스러운가?
