# Daily Idea Log (2026-01-17)

## 1. Discovery (Ideas)

| 아이디어명 | 적용 단계 | 해결하는 문제 | 제품 가치 |
| :--- | :--- | :--- | :--- |
| **1. 플레이스타일 상세 스탯 시각화 (Playstyle Dimension Radar)** | 분석 결과 (SummonerDetail) | '시야 사령관' 같은 태그가 부여된 구체적인 근거(데이터)를 알 수 없음. | 단순한 텍스트 태그를 넘어, 유저의 플레이 성향을 정량적 그래프로 보여주어 설명력(Explainability) 강화. |
| **2. 태그 설명 툴팁 (Tag Inspector)** | 분석 결과 (SummonerDetail) | 태그의 획득 조건(예: "시야 점수 상위 10%")을 알기 어려움. | 분석 로직의 투명성을 높이고, 유저가 어떤 지표를 개선해야 할지 가이드 제공. |
| **3. 매치 리스트 역할 필터** | 매치 기록 조회 | 여러 라인을 가는 유저의 경우, 특정 라인의 기록만 모아보고 싶음. | 기본적인 UX 편의성 증대 및 역할별 성과 비교 용이. |
| **4. AI 분석 프롬프트 고도화 (Raw Data 주입)** | AI 분석 | AI가 단순히 "잘했습니다" 정도의 피상적인 조언만 할 수 있음. | `DimensionScores`의 세부 수치를 AI에 제공하여 "초반 교전 지향적이나 후반 성장력이 부족합니다" 같은 구체적 코칭 유도. |
| **5. 챔피언별 플레이스타일 적합도** | 챔피언 추천 | 내 플레이스타일(예: 로밍형)과 내가 주로 하는 챔피언의 상성이 맞는지 모름. | 단순 승률 기반이 아닌, 성향 기반의 개인화된 챔피언 추천 시스템 구축 초석. |

## 2. Triage

### **Selection: 1. 플레이스타일 상세 스탯 시각화 (Playstyle Dimension Radar)**

**선정 이유:**
- **Insight Depth**: 현재 백엔드(`playstyle_tags.py`)에서 15가지 이상의 정교한 지표(`earlyAggro`, `lateCarry` 등)를 계산하고 있으나, 이를 태그 생성용으로만 쓰고 버리고 있음. 이 데이터를 시각화하는 것만으로도 제품의 깊이가 크게 향상됨.
- **Feasibility**: 이미 계산 로직이 존재하므로, 저장 로직과 프론트엔드 차트 추가만으로 구현 가능. 가성비가 매우 높음.
- **Portfolio Value**: 단순한 KDA 보여주기를 넘어, 자체 알고리즘으로 분석된 '게이머 성향'을 시각화하는 것은 포트폴리오로서 기술적 매력이 큼.

**미선정 이유:**
- **2. 태그 설명 툴팁**: 좋지만, 데이터를 먼저 시각화(1번)한 후 덧붙이는 것이 자연스러움.
- **3. 매치 리스트 필터**: 평범한 기능(Utility)이며, '분석 서비스'로서의 차별점은 약함.
- **4. AI 고도화**: 사용자 눈에 즉각적으로 보이지 않는 백엔드 로직 개선임. 1번이 선행되면 자연스럽게 연계 가능.
- **5. 챔피언 적합도**: 로직 설계가 복잡하여 당장의 MVP 범위로 부적합.

## 3. Spec Draft

### Feature: Playstyle Dimension Radar
**Problem Statement:**
유저는 자신에게 부여된 '플레이스타일 태그'의 근거를 알 수 없으며, 자신이 육각형 플레이어인지 특정 분야 특화 플레이어인지 한눈에 파악하기 어렵다.

**MVP Scope:**
- **Backend**:
  - `compute_playstyle_tags_for_summoner` 함수에서 주 포지션의 `DimensionScores` (Aggro, Vision, Farm, Objective, Teamfight, Survivability 등 6축)를 반환하도록 수정.
  - `SummonerPlaystyleTag` 모델에 `dimension_scores` (JSON) 필드 추가 및 저장.
  - API 응답 모델에 해당 점수 포함.
- **Frontend**:
  - `Recharts`를 사용하여 `PlaystyleRadarChart` 컴포넌트 신규 개발.
  - `SummonerDetail` 페이지 내, 기존 `RoleRadarChart` 하단 또는 옆에 배치.
  - 6개 축: `공격성(Aggro)`, `성장력(Farm/Growth)`, `시야(Vision)`, `오브젝트(Object)`, `팀파이트(Teamfight)`, `생존(Risk 역수)`.

**Acceptance Criteria:**
1. 소환사 상세 페이지 진입 시, 플레이스타일 태그와 함께 **육각형 레이더 차트**가 표시되어야 한다.
2. 차트의 각 축은 0.0 ~ 1.0 사이의 값으로 정규화되어 표현되어야 한다.
3. 데이터가 없는 경우(신규 유저) 차트가 비어있거나 안내 메시지가 나와야 한다.
4. "매치데이터 업데이트" 버튼 클릭 시, 차트 데이터도 함께 갱신되어야 한다.

## 4. Backlog Draft

### Title: `[Daily][2026-01-17] Playstyle Dimension Radar 구현`

### Tasks
**Backend**
- [ ] `DimensionScores` 데이터를 `SummonerPlaystyleTag` DB 모델에 저장하도록 스키마 및 로직 수정.
- [ ] `PlaystyleTagSnapshot` Pydantic 모델에 `dimension_data` 필드 추가.
- [ ] 주요 6대 지표(Aggro, Farm, Vision, Objective, Teamfight, Survival) 추출 및 정규화 로직 작성.

**Frontend**
- [ ] `api.ts` 타입 정의 업데이트 (`PlaystyleTagSnapshot` 내 `dimension_data`).
- [ ] `components/PlaystyleRadarChart.tsx` 구현 (Recharts 활용, 커스텀 축 라벨).
- [ ] `SummonerDetail.tsx` UI 레이아웃 조정 및 차트 연동.

## 5. Docs / Notes

### Suggested README Update
- **Features** 섹션에 "Advanced Playstyle Metrics Visualization" 항목 추가.
- "단순 KDA가 아닌, 15가지 세부 지표를 기반으로 한 6각 플레이스타일 분석 그래프 제공" 문구 추가.

### Questions for Next Cycle
1. 15개 세부 지표를 6개 축으로 매핑하는 가중치 로직이 적절한가? (예: `Growth` = Farm * 0.7 + Gold * 0.3 ?)
2. 역할군(포지션)별로 차트의 기준(표준)이 달라야 하는가? (서포터의 '성장력'은 라이너와 다르다. 현재는 절대값 기준임)
3. 모바일 뷰에서 차트 2개(Role, Playstyle) 배치를 어떻게 최적화할 것인가?
