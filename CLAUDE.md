# playbook-skills

Claude Code 플러그인 저장소다. 스킬 본문은 `plugins/playbook-skills/skills/*/SKILL.md` 에 있다.

## 문서 규약

- 이 저장소의 설계 결정은 `README.md` 의 "설계 원칙" 절에 "이 결정을 뒤집으려면" 조건과 함께 적는다. 별도 ADR 디렉터리를 두지 않는다.
- 여러 세션에 걸친 작업의 handoff 는 `docs/handoffs/active/<workstream>.md` 에 둔다.
- `plugins/playbook-skills/evals/**` 는 eval 픽스처다. 그 안의 `AGENTS.md`, `adr/`, `docs/handoffs/` 는 이 저장소의 문서가 아니므로 탐지 대상에서 제외한다.

## 검증

스킬 본문이나 description 을 바꾸면 eval 을 다시 돌린다. 명령은 `scripts/eval.sh` 를 쓴다.
