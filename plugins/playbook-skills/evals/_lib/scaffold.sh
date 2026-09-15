#!/usr/bin/env bash
# 케이스의 fixture/ 를 빈 워크스페이스(cwd)에 복사해 독립 git 저장소로 만든다.
# 케이스에 patch.diff 가 있으면 커밋 뒤에 적용해 "미커밋 변경이 있는 상태"를 만든다.
#
#   bash _lib/scaffold.sh <케이스 디렉터리>
#
# claude plugin eval --scaffold 가 각 케이스의 fixture.sh 를 통해 호출한다.
# 수동으로 픽스처를 살펴볼 때는 빈 디렉터리에서 직접 실행해도 된다.
set -euo pipefail
case_dir="${1:?사용법: scaffold.sh <케이스 디렉터리>}"

cp -R "$case_dir/fixture/." .
git init -q
git add -A
git -c user.email=eval@local -c user.name=eval commit -qm init
if [ -f "$case_dir/patch.diff" ]; then
  git apply "$case_dir/patch.diff"
fi
