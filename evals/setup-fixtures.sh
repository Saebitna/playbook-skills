#!/usr/bin/env bash
# 검증용 픽스처를 임시 디렉터리에 재구성한다.
# 각 픽스처는 독립 git 저장소이며, 일부는 "미커밋 변경이 있는 상태"가 설계의 일부다.
#
#   ./evals/setup-fixtures.sh /tmp/pb-eval
#
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
out="${1:?사용법: setup-fixtures.sh <출력 디렉터리>}"
mkdir -p "$out"

for src in "$here"/fixtures/*/; do
  name="$(basename "$src")"
  dst="$out/$name"
  rm -rf "$dst"; mkdir -p "$dst"
  cp -R "$src." "$dst/"
  git -C "$dst" init -q
  git -C "$dst" add -A
  git -C "$dst" -c user.email=eval@local -c user.name=eval commit -qm init
  # 픽스처 설계상 필요한 미커밋 변경
  patch_file="$here/patches/$name.patch"
  [ -f "$patch_file" ] && git -C "$dst" apply "$patch_file"
  echo "$dst"
done
