# Daily Feature Planning - 2026-01-14

## 1. Discovery (Ideas)

### 1. 플레이 스타일 태그 상세 설명 (Tag Explainability)
- **위치**: `SummonerDetail` 페이지의 플레이 스타일 태그 섹션
- **문제**: 사용자는 자신에게 "초반 주도형" 태그가 붙었을 때, 구체적으로 어떤 수치가 이 태그를 유발했는지 알 수 없음.
- **가치**: 분석 결과의 투명성을 높이고, 사용자가 자신의 강점을 데이터 기반으로 이해하게 도움. "설명 가능한 AI/분석"이라는 제품 철학에 부합.

### 2. 정교화된 Mock AI 분석 (Enhanced Mock AI)
- **위치**: `SummonerDetail` 및 `TeamBuilder`의 AI 분석 텍스트
- **문제**: 현재 `MockAIProvider`는 고정된 텍스트만 반환하여, API 키가 없는 환경(포트폴리오 데모 등)에서 기능의 역동성을 보여주기 어려움.
- **가치**: 간단한 규칙 기반(Heuristic) 텍스트 생성을 통해, Mock 환경에서도 실제 데이터에 반응하는 듯한 경험을 제공.

### 3. 라인 맞상대 비교 뷰 (Lane Matchup Comparison)
- **위치**: `SummonerDetail`의 매치 상세(Match Detail) 다이얼로그
- **문제**: 매치 상세 정보가 팀별로 나열되어 있어, 실제 내 라인 맞상대와의 지표(CS, 골드 등) 격차를 한눈에 파악하기 어려움.
- **가치**: LoL 사용자에게 가장 직관적인 "라인전 승패"를 정량적으로 보여주어 분석 깊이를 더함.

### 4. 최근 성적 추세선 (Recent Performance Sparkline)
- **위치**: `RoleRadarChart` 하단 또는 Role별 카드 내부
- **문제**: 현재 평균 점수만 보여주어, 최근 실력이 상승세인지 하락세인지 파악 불가능.
- **가치**: 시계열 변화를 시각화하여 사용자가 자신의 성장 과정을 추적할 수 있게 함.

### 5. 매치 임팩트 태그 (Match Impact Tags)
- **위치**: 매치 리스트의 각 매치 카드
- **문제**: 승/패와 KDA만으로는 해당 판에서 내가 얼마나 결정적인 역할을 했는지(예: "ACE", "딜량 1등", "역전승") 알기 어려움.
- **가치**: 리스트 뷰에서 직관적인 성취감을 제공하고 클릭 유도.

---

## 2. Triage

### Top 1: 플레이 스타일 태그 상세 설명 (Tag Explainability)
- **선정 이유 (ICE Reasoning)**
  - **Impact (High)**: 이 프로젝트의 핵심 차별점인 "Tag 시스템"의 신뢰도를 크게 높임. 사용자가 가장 궁금해하는 "왜?"를 해소.
  - **Confidence (High)**: 백엔드에 이미 계산 로직(`weights`, `threshold`)이 존재하므로, 이를 API에 노출하기만 하면 됨.
  - **Ease (High)**: 복잡한 DB 스키마 변경 없이 API 응답 모델과 프론트엔드 툴팁 추가로 구현 가능.
- **탈락 아이디어 회고**
  - **라인 맞상대 비교**: 상대 라이너를 정확히 특정하는 로직(Riot API의 포지션 데이터 불안정성 보정 등)이 선행되어야 하여 공수가 큼.
  - **Mock AI 정교화**: 좋은 아이디어이나, Tag 시스템의 설명력을 높이는 것이 현재의 "분석 깊이" 목표에 더 부합함.

---

## 3. Spec Draft (Top 1)

### Feature Name
플레이 스타일 태그 상세 설명 (Playstyle Tag Explainability)

### Problem Statement
사용자는 시스템이 부여한 "플레이 스타일 태그"의 근거를 알 수 없어, 분석 결과에 대한 신뢰도가 낮거나 자신의 플레이를 어떻게 개선/유지해야 할지 구체적인 피드백을 얻기 어렵다.

### MVP Scope
1. **Backend**: `compute_playstyle_tags_for_summoner` 및 관련 API 응답에 `score` (계산된 점수), `threshold` (기준 점수), `contribution` (주요 기여 지표 및 가중치) 정보를 포함.
2. **Frontend**: 태그 칩(Chip) 클릭 또는 호버 시 `Popover`를 띄워 상세 정보를 표시.
   - 예: "초반 주도형 (Score: 0.82 / Cut: 0.7)"
   - 기여 요인: "Early Aggro (50%), Lane Lead (30%)"

### Optional Scope
- 태그 점수가 기준치에 거의 도달했지만 아깝게 획득하지 못한 "잠재적 태그" 표시.

### Acceptance Criteria
- [ ] `GET /summoners/{name}/playstyle` 응답의 각 태그 객체에 `score`, `threshold`, `detail_text` 필드가 포함되어야 한다.
- [ ] `SummonerDetail` 페이지에서 태그를 클릭하면 팝오버(또는 툴팁)가 열려야 한다.
- [ ] 팝오버 내부에는 "계산 점수 vs 기준 점수"와 "주요 평가 항목"이 명시되어야 한다.
- [ ] 모바일 환경에서도 터치 시 툴팁 내용을 확인할 수 있어야 한다.

---

## 4. Backlog Draft

### Title
[Daily][2026-01-14] Implement Playstyle Tag Explainability

### Tasks
1. **[Backend] 태그 계산 로직 반환값 확장**
   - `evaluate_tags_for_role` 함수가 단순 태그 ID뿐만 아니라 계산된 `score`와 매칭된 `TagDefinition`의 메타데이터를 함께 반환하도록 수정.
2. **[Backend] API 스키마 업데이트**
   - `PlaystyleTag` Pydantic 모델에 `score`, `threshold`, `description` 필드 추가.
3. **[Frontend] TagDetailTooltip 컴포넌트 구현**
   - MUI `Popover` 또는 `Tooltip`을 활용하여 태그 상세 정보를 보여주는 컴포넌트 제작.
4. **[Frontend] SummonerDetail 연동**
   - 태그 리스트 렌더링 부분에 위 컴포넌트 적용 및 클릭 이벤트 핸들링.

---

## 5. Docs / Notes

### README Update Suggestion
- **Section**: "Key Features"
- **Content**: "Transparent Analysis: Click on any playstyle tag to see exactly how it was calculated based on your in-game metrics."

### Questions & Uncertainties
1. 태그 계산 공식이 복잡해질 경우(예: 비선형 가중치), 현재의 단순 `weights` 필드만으로 설명이 충분할지?
2. 모바일 뷰에서 툴팁이 화면을 가리는 UX 문제를 어떻게 우아하게 해결할지? (Bottom Sheet 고려)
3. 다국어 지원 시 기여 요인(Dimension 이름)의 한글화 처리는 어디서 담당할지? (현재는 백엔드 `label_ko`만 존재)
