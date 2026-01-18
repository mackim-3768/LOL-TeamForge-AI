# Daily Idea Log: 2026-01-18

## 1. Discovery (Ideas)
1. **플레이스타일 태그 상세 보기 (Playstyle Tag Detail View)**
   - **User Flow**: 소환사 상세 페이지(SummonerDetail) > 태그 목록
   - **Problem**: 사용자는 자신에게 부여된 태그(예: 'Aggressive')가 어떤 기준으로 산정되었는지 알 수 없어 분석 결과를 신뢰하기 어렵다.
   - **Why**: 분석의 '근거'를 제시함으로써 Explainability를 강화하고 포트폴리오 가치를 높인다.

2. **최근 20게임 지표 트렌드 그래프 (Match Trend Graph)**
   - **User Flow**: 소환사 상세 페이지 > 전적 리스트 상단
   - **Problem**: 단순 평균 지표만으로는 최근 실력의 상승/하락세나 기복을 파악하기 어렵다.
   - **Why**: 시각적인 Insight를 제공하여 단순 데이터 나열보다 풍부한 UX를 제공한다.

3. **AI 분석 프롬프트/응답 디버그 모드 (AI Debug Mode)**
   - **User Flow**: Admin 페이지 또는 소환사 상세 페이지(Admin 권한)
   - **Problem**: AI 분석 결과가 어떻게 도출되었는지(프롬프트 내용) 확인하고 싶을 때 로그를 뒤져야 한다.
   - **Why**: AI 연동 로직의 투명성을 보여줄 수 있어 기술 포트폴리오로서의 가치가 높다.

4. **유사 소환사 찾기 (Similar Summoner Finder)**
   - **User Flow**: 소환사 상세 페이지 > 사이드바
   - **Problem**: 자신의 플레이스타일이 프로게이머나 다른 고수들과 얼마나 비슷한지 비교하고 싶다.
   - **Why**: 사용자의 호기심을 자극하고 서비스 체류 시간을 늘릴 수 있는 재미 요소다.

5. **상세 수집 진행 상태 표시 (Detailed Collection Progress)**
   - **User Flow**: 소환사 등록/갱신 로딩 화면
   - **Problem**: 데이터 수집 시간이 길어질 때 단순 스피너만으로는 진행 상황(멈춘 건지, 되고 있는 건지)을 알 수 없다.
   - **Why**: 대기 시간의 체감 지루함을 줄이고 시스템 상태를 명확히 전달하여 UX를 개선한다.

## 2. Triage
- **Selection**: **플레이스타일 태그 상세 보기 (Playstyle Tag Detail View)**
- **Reasoning**:
  - **Explainability (High)**: 사용자가 가장 궁금해할 '분석 근거'를 직접적으로 해소해준다.
  - **Feasibility (High)**: 백엔드에서 이미 계산된 점수(`DimensionScores`)를 활용하므로 프론트엔드 작업 위주로 구현 가능하다.
  - **Priority**: 트렌드 그래프나 디버그 모드보다 '핵심 분석 결과의 설득력'을 높이는 것이 제품의 본질적 가치에 더 기여한다.
- **Why others skipped**:
  - 트렌드 그래프: `recharts` 라이브러리 활용 등 공수가 상대적으로 크며, 태그 시스템의 완성이 우선이다.
  - AI 디버그 모드: 일반 사용자에게는 불필요한 정보일 수 있어 우선순위가 낮다.

## 3. Spec Draft (Top 1)
- **Feature Name**: 플레이스타일 태그 상세 보기 (Playstyle Tag Detail View)
- **Problem Statement**: 사용자는 태그의 선정 기준과 자신의 점수를 알 수 없어 분석 결과를 100% 신뢰하지 못한다.
- **MVP Scope**:
  - 태그 칩(Chip) 클릭 시 팝오버(Popover) 호출
  - 해당 태그의 정의(Definition)와 연관된 Dimension Score 표시 (예: 10점 만점에 8.5점)
  - 태그별 간단한 설명 텍스트 제공
- **Optional Scope**:
  - 전체 사용자 분포 대비 백분위 표시 (통계 데이터 필요 시 제외)
- **Acceptance Criteria**:
  1. 소환사 상세 페이지의 태그 리스트에서 각 태그를 클릭할 수 있어야 한다.
  2. 클릭 시 팝오버가 나타나며, 태그 이름, 설명, 점수(Score)가 명확히 보여야 한다.
  3. 팝오버 외부 영역을 클릭하면 팝오버가 닫혀야 한다.

## 4. Backlog Draft
- **Suggested GitHub Issue Title**: `[Daily][2026-01-18] 플레이스타일 태그 상세 정보(근거 점수) UI 구현`
- **Task Breakdown**:
  1. [Frontend] `TagDefinition` 인터페이스에 태그별 설명(description) 및 관련 점수 키(key) 매핑 데이터 추가
  2. [Frontend] 태그 클릭 시 상세 정보를 보여줄 `TagDetailPopover` 컴포넌트 구현 (MUI Popover 활용)
  3. [Frontend] `SummonerDetail` 페이지의 태그 칩에 `onClick` 이벤트 핸들러 및 Popover 연동
  4. [Frontend] 디자인 폴리싱 (타이포그래피, 간격 조정)

## 5. Docs / Notes
- **Suggested README update**: '주요 기능' 섹션에 "플레이스타일 분석 및 상세 근거(지표 점수) 제공" 문구 추가
- **Questions**:
  1. `SummonerResponse` API 응답에 현재 태그별 기여 점수(contribution score)가 포함되어 있는지 확인이 필요하다. (없다면 프론트에서 `dimension_scores`를 조회하여 매핑해야 함)
  2. 모바일 환경에서 툴팁/팝오버 인터랙션이 매끄러운지 테스트가 필요하다.
  3. 태그 설명 텍스트를 하드코딩할지 백엔드에서 내려줄지 아키텍처 결정이 필요하다. (MVP는 하드코딩 권장)
