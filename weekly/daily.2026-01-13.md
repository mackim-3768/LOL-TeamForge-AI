# Weekly Ideas Log - 2026-01-13

## 1. Discovery (Ideas)

### 1. Duo Synergy Radar Comparison (듀오 시너지 레이더 비교)
- **User Flow**: Duo Synergy Tool (결과 화면)
- **Problem**: "시너지 점수: 60점"이라는 결과만으로는 불투명함. 사용자는 왜 자신의 스타일이 파트너와 안 맞는지, 혹은 잘 맞는지 알 수 없음. "나의 공격성 vs 너의 공격성"을 직관적으로 비교할 수 없음.
- **Relevance**: "Explainability(설명 가능성)"을 크게 향상시킴. 시너지 점수 뒤에 숨겨진 수학적 근거를 시각화함.

### 2. Playstyle Tag Detail Modal (플레이스타일 태그 상세 모달)
- **User Flow**: Summoner Detail Page (태그 클릭 시)
- **Problem**: 사용자는 "섬 파밍형 탑" 같은 태그를 보지만, 정확한 기준(예: "Farm Focus > 0.6, Roam < 0.2")을 알지 못함.
- **Relevance**: 분석 기준과 사용자의 실제 수치를 대조해 보여줌으로써 분석 결과에 대한 신뢰도를 높임.

### 3. Champion-Specific Playstyle Tags (챔피언별 플레이스타일 태그)
- **User Flow**: Summoner Detail Page -> Champion Filter
- **Problem**: 사용자가 레넥톤으로는 "공격적 다이버"일 수 있지만, 케일로는 "안전 성장형"일 수 있음. 현재의 글로벌 태그는 이를 평균화하여 보여줌.
- **Relevance**: 챔피언별 숙련도의 뉘앙스를 드러내어 "Insight Depth(통찰의 깊이)"를 더함.

### 4. "Golden Match" Highlighter (인생 경기 하이라이터)
- **User Flow**: Summoner Detail Page -> Match History
- **Problem**: 사용자는 자신의 "최고점 퍼포먼스"가 어떤 모습인지 수치적으로 확인하고 싶어 함.
- **Relevance**: 긍정적인 강화(Positive reinforcement)를 제공하며, 계산된 점수를 기반으로 최고의 경기를 강조함.

### 5. Recent Performance Trend Graph (최근 퍼포먼스 트렌드 그래프)
- **User Flow**: Summoner Detail Page
- **Problem**: 단순 평균값은 최근의 실력 향상이나 슬럼프를 숨김.
- **Relevance**: 지난 20경기 동안 플레이어가 성장하고 있는지, 혹은 틸트(Tilt) 상태인지 시계열로 보여줌.

---

## 2. Triage

### Selected Feature: **Duo Synergy Radar Comparison**

**Why selected?**
- **High Impact**: 호환성을 시각화하는 것은 듀오 툴의 "킬러 기능"임. 블랙박스 같은 점수를 "우리는 둘 다 시야 점수가 낮으니 이걸 고쳐보자"와 같은 실행 가능한 대화 주제로 바꿔줌.
- **Feasibility**: `recharts` 라이브러리가 이미 설치되어 있음. 백엔드 로직(`DimensionScores`)도 존재하므로 이를 노출하기만 하면 됨.
- **Portfolio Value**: 풀스택 역량(API 설계 + 데이터 시각화)을 보여주기에 적합함.

**Why others were not selected?**
- **Playstyle Tag Detail Modal**: 매우 좋은 아이디어지만, 레이더 차트 비교보다는 시각적 임팩트가 덜함. 다음 사이클의 유력 후보임.
- **Champion-Specific Tags**: 챔피언 그룹별로 태그를 다시 계산해야 하므로 백엔드 리팩토링 범위가 큼. 복잡도가 높음.
- **Golden Match**: 있으면 좋지만(Nice to have), 듀오 툴만큼 상호작용적인 기능은 아님.

---

## 3. Spec Draft: Duo Synergy Radar Comparison

### Feature Name
Duo Synergy Radar Comparison (듀오 시너지 레이더 비교)

### Problem Statement
현재 `DuoSynergyTool`은 "스타일 시너지(예: 초반 라인전 40%)"에 대한 점수만 제공할 뿐, 왜 40점인지 설명하지 않음. 사용자는 두 소환사의 개별 스탯을 나란히 비교하여 구체적인 차이점이나 공통점을 파악할 수 없음.

### MVP Scope
- **Backend**: `compute_duo_synergy` 함수(및 API 응답)를 수정하여 두 소환사의 정규화된 `DimensionScores`(`summoner1_stats`, `summoner2_stats`)를 반환하도록 함.
- **Frontend**: `recharts`를 사용하여 `SynergyRadarChart` 컴포넌트를 추가함.
- **UI**: `DuoSynergyTool` 결과 화면에서 점수 하단에 차트를 표시함. 두 소환사의 다각형을 [Aggro, Farm, Vision, Objective, Roam, Teamfight] 축 위에 오버레이하여 표시함.

### Acceptance Criteria
1. **API Response**: `GET /duo-synergy` 응답은 반드시 정규화된(0.0-1.0) 값을 가진 `summoner1_stats`와 `summoner2_stats` 객체를 포함해야 함.
2. **Visualization**: `DuoSynergyTool` 페이지는 두 개의 다각형(서로 다른 색상, 범례 포함)이 있는 Radar Chart를 표시해야 함.
3. **Data Accuracy**: 데이터 포인트에 마우스를 올리면(Hover) 소환사 A와 B의 정확한 수치를 툴팁으로 보여줘야 함.
4. **Resilience**: 한 소환사의 게임 수가 0이거나 데이터가 비어 있어도 차트가 깨지지 않고(0점으로 표시) 정상 동작해야 함.

---

## 4. Backlog Draft

### Title
[Daily][2026-01-13] Duo Synergy Radar Comparison 구현

### Tasks
1. **Backend**: `backend/core_api/duo_synergy.py`의 `compute_duo_synergy`를 수정하여 두 소환사의 `DimensionScores`를 반환하도록 변경.
2. **Backend**: `backend/core_api/main.py`(또는 라우터 정의 파일)의 `DuoSynergyResponse` 스키마를 업데이트하여 새 필드 포함.
3. **Frontend**: `frontend/src/api.ts`의 `DuoSynergyResponse` 타입을 API 응답에 맞춰 업데이트.
4. **Frontend**: `frontend/src/components/` 경로에 `recharts`를 활용한 `SynergyRadarChart` 컴포넌트 생성.
5. **Frontend**: `frontend/src/pages/DuoSynergyTool.tsx`에 차트 통합 및 UI 배치.

---

## 5. Docs / Notes

### README Update
- **Section**: Features -> Duo Analysis
- **Content**: "두 소환사 간의 플레이스타일 차이를 시각화하는 인터랙티브 레이더 차트 비교 기능 추가."

### Questions for Next Cycle
1. 축(Axis)의 색상을 "시너지 영향도"에 따라 다르게 표시해야 할까? (예: 시야 점수 차이가 크면 시야 축을 강조 표시)
2. 모바일 레이아웃에서 레이더 차트의 크기와 가독성을 어떻게 확보할 것인가? (MUI Grid `xs={12}`를 쓰더라도 차트 자체의 크기 조정 필요)
3. 이 스탯 데이터를 기반으로 "추천 챔피언 조합"을 제안하는 기능을 나중에 추가할 수 있을까?
