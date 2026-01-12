# Daily Idea Log (2026-01-12)

## 1. Discovery (Ideas)

### 1. 플레이스타일 다차원 분석 레이더 차트 (Playstyle Dimension Radar)
- **위치**: `SummonerDetail` 페이지, 플레이스타일 태그 하단
- **문제**: 현재 플레이스타일 태그(예: "초반 주도형")는 단편적인 결과만 보여줄 뿐, 유저의 전반적인 성향(공격성 vs 안정성 등)을 한눈에 파악하기 어렵습니다.
- **중요성**: 태그 산출에 사용되는 `DimensionScores` (공격성, 시야, 성장 등) 데이터를 시각화함으로써 분석의 설득력을 높이고 유저에게 더 깊은 인사이트를 제공합니다.

### 2. 태그 부여 원인 설명 툴팁 (Tag Reasoning Tooltip)
- **위치**: 플레이스타일 태그 칩(Chip) 호버 시
- **문제**: "왜 내가 '시야 사령관'인가?"에 대한 구체적 수치가 드러나지 않아 분석 신뢰도가 떨어질 수 있습니다.
- **중요성**: "내 점수 0.8 / 기준 0.7"과 같이 구체적 수치를 보여주어 시스템의 투명성(Explainability)을 강화합니다.

### 3. 매치 리스트 '임팩트 배지' (Match Impact Badge)
- **위치**: 최근 매치 리스트의 각 매치 카드
- **문제**: 승/패와 KDA만으로는 해당 게임에서 내가 얼마나 결정적인 역할을 했는지(Hard Carry vs Bus) 알기 어렵습니다.
- **중요성**: OP Score나 딜 비중을 기반으로 "ACE", "딜 1등", "타워 철거반" 등의 배지를 달아주어 리스트 탐색 경험을 개선합니다.

### 4. 역할군별 퍼포먼스 추이 그래프 (Role Performance Trend)
- **위치**: `SummonerDetail` 페이지 하단
- **문제**: 최근 20게임 동안 내 폼이 오르고 있는지, 떨어지고 있는지 직관적으로 알 수 없습니다.
- **중요성**: 단순 평균값이 아닌 '추세'를 보여줌으로써 유저의 성장을 시각화합니다.

### 5. 매치 상세 '골드/경험치 차이' 시각화 (Match Detail Advantage Graph)
- **위치**: 매치 상세 다이얼로그 (`MatchDetail`)
- **문제**: 최종 아이템과 KDA만으로는 게임의 흐름(역전승인지 압살인지)을 파악하기 어렵습니다.
- **중요성**: (Riot API 타임라인 데이터 활용 가능 시) 시간대별 골드 차이를 그래프로 보여주어 게임의 서사를 전달합니다.

---

## 2. Triage

### Selected: 플레이스타일 다차원 분석 레이더 차트 (Playstyle Dimension Radar)

**선정 이유 (ICE Reasoning)**
- **Impact (High)**: 텍스트 기반 태그보다 시각적 임팩트가 크며, "데이터 기반 분석"이라는 제품의 정체성을 가장 잘 보여줍니다. 숨겨진 `DimensionScores` 데이터를 활용하여 정보의 깊이를 더합니다.
- **Confidence (High)**: 이미 백엔드 `playstyle_tags.py` 내부에서 `DimensionScores`를 계산하고 있습니다. 프론트엔드에는 `recharts` 라이브러리가 이미 설치되어 있어 구현 리스크가 낮습니다.
- **Ease (Medium)**: 백엔드 API 응답 스키마 수정과 프론트엔드 차트 컴포넌트 추가 작업이 필요하지만, 구조적으로 복잡하지 않습니다.

**탈락된 아이디어 (Brief)**
- **태그 툴팁**: 유용하지만 시각적 재미가 덜합니다. 레이더 차트가 구현되면 그 안에 포함되거나 보조적으로 들어갈 수 있습니다.
- **임팩트 배지**: 배지 선정 로직(기준값) 정의가 까다롭고 주관적일 수 있습니다.
- **추이 그래프**: 20게임 표본으로는 유의미한 추세를 보기 힘들 수 있습니다.
- **골드 그래프**: Riot API의 Timeline 데이터를 추가로 가져와야 할 수도 있어(확인 필요) 구현 비용이 높습니다.

---

## 3. Spec Draft

### Feature: Playstyle Dimension Radar Visualization

#### Problem Statement
현재 `SummonerDetail` 페이지는 플레이스타일 태그를 단순히 나열만 하고 있어, 유저가 자신의 플레이 성향을 입체적으로(예: 공격적이면서 시야도 잘 잡는지, 아니면 성장만 하는지) 파악하기 어렵습니다. 백엔드에서 계산하는 정교한 6~15가지 지표가 사용자에게 전달되지 않고 소실되고 있습니다.

#### MVP Scope
1.  **Backend (`playstyle_tags.py`)**
    -   `compute_playstyle_tags_for_summoner` 함수가 태그뿐만 아니라 주 포지션의 `DimensionScores`(Raw Values)도 반환하도록 수정합니다.
    -   API 응답(`PlaystyleTagSnapshot`)에 `dimensions` 필드를 추가합니다.
2.  **Frontend (`SummonerDetail.tsx`)**
    -   `recharts` 라이브러리의 `Radar`, `RadarChart`, `PolarGrid` 등을 사용하여 6각형 레이더 차트를 구현합니다.
    -   축(Axis): 공격(Aggro), 안정(Stability/Risk의 역수), 시야(Vision), 성장(Farm), 전투(Damage), 운영(Map/Objective) - *초안이며 데이터 상황에 따라 조정*
    -   태그 섹션 우측 또는 하단에 배치합니다.

#### Optional Scope
- 각 축에 마우스 오버 시 상세 수치(0.0~1.0) 및 설명 툴팁 표시
- "비슷한 티어 평균" 데이터와 비교 (데이터 확보 어려움으로 후순위)

#### Acceptance Criteria
- [ ] `GET /summoners/{name}/playstyle` 응답에 `dimensions` 객체가 포함되어야 한다.
- [ ] `SummonerDetail` 페이지 진입 시, 플레이스타일 태그와 함께 레이더 차트가 렌더링되어야 한다.
- [ ] 레이더 차트는 최소 5개 이상의 축을 가져야 하며, 데이터가 없는 경우(0 게임) 적절한 빈 상태(Empty State)를 보여주어야 한다.

---

## 4. Backlog Draft

### Title: [Daily][2026-01-12] 플레이스타일 레이더 차트 시각화 구현

#### Tasks
1.  **[Backend] Playstyle API 응답 스키마 확장**
    -   `backend/core_api/playstyle_tags.py`: `compute_playstyle_tags_for_summoner`에서 `DimensionScores`를 반환하도록 수정
    -   `DimensionScores` 데이터를 DB `SummonerPlaystyleTag.tags` JSON에 포함하거나 별도 컬럼/필드로 처리 (JSON 확장이 유리)
2.  **[Frontend] PlaystyleRadarChart 컴포넌트 개발**
    -   `frontend/src/components/PlaystyleRadarChart.tsx` 생성
    -   `recharts` 활용하여 `DimensionScores` 데이터를 시각화
3.  **[Frontend] SummonerDetail 페이지 통합**
    -   API 연동부 수정 및 차트 배치
    -   모바일/데스크탑 반응형 레이아웃 조정

---

## 5. Docs / Notes

### Suggested README Update
- **Features 섹션**: "AI 기반 플레이스타일 태그 분석" 항목에 "다차원 성향 분석 차트(Playstyle Radar)" 내용을 추가하여 시각화 기능을 강조합니다.

### Next Cycle Exploration
1.  `DimensionScores`의 값들이 0.0~1.0 사이로 잘 정규화되어 분포하는지 실제 데이터로 확인 필요 (너무 0.1에 몰려있으면 그래프가 안 예쁨).
2.  `recharts`의 Radar Chart가 모바일 화면에서 잘 줄어드는지 확인 필요.
3.  현재 `TagDefinition`에 있는 가중치(weights)를 역으로 추적해서 "이 태그가 왜 나왔는지" 설명해주는 기능의 구현 가능성 검토.
