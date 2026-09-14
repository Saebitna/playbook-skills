#!/usr/bin/env bash
# playbook-skills eval 스위트 실행. 추가 인자는 그대로 전달한다.
#
#   scripts/eval.sh                      # 전체 (케이스당 3회, baseline 비교)
#   scripts/eval.sh --case f3-closeout   # 한 케이스
#   scripts/eval.sh --runs 1 --ablation none
#
# --judge-model sonnet: 기본 judge(haiku)가 긴 한국어 보고를 오판한 사례가 있다.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
exec claude plugin eval "$root/plugins/playbook-skills" \
  --scaffold \
  --allow-tools Bash Edit Write \
  --judge-model sonnet \
  "$@"
