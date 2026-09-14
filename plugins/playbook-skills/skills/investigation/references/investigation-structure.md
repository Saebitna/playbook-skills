# Investigation 문서 구조

문서 상단은 한 번만 쓰고, 실험 로그는 실험마다 누적한다.

```markdown
# <문제 요약>
Status: active | resolved | abandoned
Last updated: YYYY-MM-DD
```

## 상단 섹션 (한 번 작성, 필요 시 갱신)

### Problem and Target

무엇이 잘못되었고, 무엇이 되면 해결로 볼 것인가. **측정 가능한 목표**를 쓴다.
나쁜 예: "느리다." 좋은 예: "`POST /rank` p95가 1.8s. 목표 300ms 이하."

### Baseline

실험 전 기준값을 고정한다. 이게 없으면 이후 측정이 의미를 갖지 못한다.

- 환경: 브랜치, 커밋, 런타임 버전, OS, 설정
- 데이터·입력: 어떤 입력으로 재현하는가
- 현재 측정값: 실패율, 지연, 에러 메시지 원문
- **재현 명령**: 그대로 실행 가능한 형태

```text
git rev-parse --short HEAD   → a1b2c3d
uv run pytest tests/test_rank.py::test_batch -x   → 5회 중 2회 실패 (flaky)
```

### Hypotheses

서로 **구분 가능한** 원인 후보를 나열하고, 각각의 근거와 예상 신호를 쓴다. 한 실험으로 둘 다 지지된다면 가설이 아직 덜 갈라진 것이다.

| # | 가설 | 근거 | 이게 참이면 나타날 신호 | 상태 |
| --- | --- | --- | --- | --- |
| H1 | ... | ... | ... | Open / Supported / Rejected |

실험 `Interpretation`과 가설 상태의 대응: `Supported` → `Supported`, `Rejected` → `Rejected`, `Inconclusive` → `Open` 유지.

## 실험 로그 (실험마다 추가)

```markdown
### Experiment N — YYYY-MM-DD

**Testing:** H<번호>
**Changed variable:** (딱 하나)
**Observation:** 이 실험을 하게 만든 관찰 사실
**Experiment:** 실행한 명령·코드 변경 (최소 범위)
**Expected Result:** 가설이 참일 때 / 거짓일 때 각각 어떤 신호가 나오는가 — 실행 전에 작성
**Actual Result:** 명령 출력, 로그, 측정값 원문
**Interpretation:** Supported | Rejected | Inconclusive + 이유
**Next:** 다음으로 정보 가치가 가장 큰 실험
```

`Expected Result`를 실행 전에 쓰는 것이 이 구조의 핵심이다. 사후에 쓰면 어떤 결과든 가설을 지지하는 것처럼 보인다.

## 하단 섹션 (누적)

### Findings

지금까지 **확인된** 사실만. 추론은 여기 넣지 않는다.

### Ruled Out

배제된 원인과 배제 근거. 다음 세션이 같은 걸 다시 시도하지 않게 한다.

### Open Questions

아직 답하지 못한 질문.

### Related Decisions

연결된 decision/ADR 경로.

## 해결 시 추가

### Root Cause

근본 원인과 그것을 지지하는 결정적 증거.

### Fix and Regression Test

최소 범위의 수정 권고와 재발을 잡을 테스트. 첫 줄에 `적용됨` 또는 `권고만`을 적는다.

### Residual Uncertainty

수정 후에도 남는 불확실성. "완전히 해결됐다"고 단정하지 않는다.
