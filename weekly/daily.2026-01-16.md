# Daily Feature Planning - 2026-01-16

## 1. Discovery (Ideas)

| ID | Feature Name | User Flow | User Problem | Value |
|:--:|:--|:--|:--|:--|
| 1 | **Playstyle Dimension Visualizer** | Summoner Detail | 사용자가 자신에게 부여된 태그(예: "초반 주도형")의 구체적인 근거(지표)를 알기 어려움 | 태그 선정의 투명성을 높이고, 사용자가 어떤 지표(공격성, 안정성 등)를 강화해야 할지 직관적으로 파악 가능 |
| 2 | **Match Detail Momentum Graph** | Match Detail | 경기 내의 흐름(골드 차이, 경험치 차이 등)을 한눈에 파악하기 어려움 | 단순히 KDA/딜량뿐만 아니라, 승패가 갈린 시점(역전 구간 등)을 시각적으로 복기 가능 |
| 3 | **AI Analysis Focus Mode** | AI Analysis | AI 분석이 너무 포괄적이어서 특정 영역(예: 라인전, 한타)에 대한 깊이 있는 조언을 얻기 힘듦 | 사용자가 관심 있는 분야(Laning, Vision 등)를 선택하여 맞춤형 피드백을 받음으로써 효용성 증대 |
| 4 | **Duo Synergy Recommender** | Team Builder | 자신의 플레이스타일과 잘 맞는 듀오 파트너의 유형을 알지 못함 | "공격적 정글러에게는 로밍형 미드가 적합"과 같은 구체적 제안을 통해 실제 듀오 매칭 확률 증대 |
| 5 | **Tier-based Metric Comparison** | Summoner Detail | 자신의 지표(CS 8.0)가 해당 티어에서 상위 몇 %인지 알 수 없음 | 단순 절대값 대신 상대적 위치를 보여줌으로써 객관적인 실력 점검 및 동기 부여 제공 |

## 2. Triage

### Top 1 Feature: **Playstyle Dimension Visualizer (플레이스타일 상세 분석 차트)**

*   **Selection Reason (ICE Score-based)**
    *   **Impact (High):** "Explainability of analysis"라는 핵심 가치를 직접적으로 강화함. 사용자가 "왜 이 태그인가?"를 이해하는 데 결정적임.
    *   **Confidence (High):** 이미 백엔드(`DimensionScores`)에서 계산하고 있는 데이터이므로, API 노출과 프론트엔드 시각화만 수행하면 됨.
    *   **Ease (Medium):** `recharts` 라이브러리가 이미 존재하며, 데이터 파이프라인 수정이 크지 않음.
    *   **Portfolio Value:** 복잡한 데이터를 시각화하여 보여주는 기능은 기술적 완성도를 높게 보이게 함.

*   **Why others were not selected**
    *   **Momentum Graph:** 타임라인 데이터(Timeline API) 확보가 선행되어야 하며, 데이터 용량이 커질 수 있음.
    *   **AI Focus Mode:** 프롬프트 엔지니어링 및 토큰 비용 증가 고려 필요.
    *   **Duo Synergy Recommender:** 소셜 기능(친구 찾기)과 연계되지 않으면 단독 기능으로는 임팩트가 약함.
    *   **Tier Comparison:** 티어별 평균 데이터(Baselines)를 수집하고 유지보수하는 별도의 배치 작업이 필요함.

## 3. Spec Draft

### Feature Name: Playstyle Dimension Radar (플레이스타일 상세 분석 차트)

### Problem Statement
사용자는 `SummonerDetail` 페이지에서 자신의 플레이스타일 태그(예: "시야 사령관")를 확인하지만, 해당 태그가 어떤 지표(시야 점수, 제어 와드 등)에 기반하여 산출되었는지 알 수 없어 분석 결과에 대한 신뢰도와 활용도가 떨어짐.

### MVP Scope
1.  **Backend:**
    *   `GET /summoners/{name}/playstyle-tags` 응답에 `DimensionScores` (Aggro, Risk, Vision, Farm, Damage, Winrate 등 6대 지표) 데이터를 포함하여 반환.
    *   값은 0.0 ~ 1.0 범위로 정규화된 상태 유지.
2.  **Frontend:**
    *   `SummonerDetail` 페이지의 태그 섹션 옆(또는 하단)에 Radar Chart 추가.
    *   차트 축: Aggro, Risk, Vision, Farm, Damage, Winrate.
    *   100점 만점 기준으로 환산하여 표시.

### Optional Scope
*   Advanced Metrics (EarlyAggro, LateCarry 등)를 보여주는 "고급 분석" 탭 추가.
*   주포지션(Primary Role) 외의 다른 포지션에 대한 차트 전환 기능.

### Acceptance Criteria
1.  `GET /summoners/{name}/playstyle-tags` 호출 시 응답 JSON에 `dimension_scores` 객체가 포함되어야 한다.
2.  프론트엔드 `SummonerDetail` 페이지 로딩 시, Playstyle Tags와 함께 Radar Chart가 렌더링되어야 한다.
3.  Radar Chart의 각 축은 0~100 스케일로 표현되며, 데이터가 없을 경우 0으로 표시되거나 차트가 비활성화되어야 한다.
4.  차트에 마우스를 올리면 구체적인 수치(Score)가 툴팁으로 표시되어야 한다.

## 4. Backlog Draft

### Suggested Title
`[Daily][2026-01-16] 플레이스타일 상세 분석 차트(Radar Chart) 구현`

### Task Breakdown
1.  **[Backend] API Response Schema Update**
    *   `PlaystyleTagSnapshotResponse` 모델에 `dimension_scores` 필드 추가.
    *   `get_playstyle_tags` 엔드포인트에서 DB의 Snapshot 데이터 내 `dimension_scores`를 파싱하여 반환하도록 로직 수정 (필요 시 DB Schema에 컬럼 추가 혹은 JSON 내 포함 확인).
    *   *Note:* 현재 DB `tags` JSON에 점수 정보가 없다면, `upsert_playstyle_snapshot` 시점에 점수도 함께 저장하도록 수정 필요.
2.  **[Frontend] PlaystyleRadarChart Component**
    *   `recharts`의 `RadarChart`를 사용하여 6각형 차트 구현.
    *   Props로 `dimension_scores`를 받아 시각화.
3.  **[Frontend] SummonerDetail Integration**
    *   기존 `RoleRadarChart`와 혼동되지 않도록 위치 선정 (Tags 영역 근처).
    *   데이터 로딩 중/에러 상태 처리.

## 5. Docs / Notes

### README Update Recommendation
*   **Section:** Features > Playstyle Analysis
*   **Message:** "단순한 태그 부여를 넘어, 공격성/안정성/시야/성장/딜링/승률 6가지 차원에서 플레이어의 성향을 시각적으로 분석하는 Radar Chart 제공."

### Questions & Uncertainties
1.  현재 `SummonerPlaystyleTag` DB 테이블의 `tags` 컬럼(JSON)에 `dimension_scores`가 함께 저장되고 있는지 확인 필요. (저장되지 않는다면 스키마 마이그레이션 혹은 로직 수정 필요)
2.  `RoleRadarChart` (포지션별 점수)와 `PlaystyleRadarChart` (플레이 성향 점수)가 한 페이지에 동시에 존재할 때 사용자에게 혼동을 주지 않도록 UI 배치를 어떻게 할 것인가?
3.  모바일 뷰포트에서 Radar Chart의 가독성 확보 방안.
