#!/usr/bin/env bash
# f3-closeout 의 픽스처를 그대로 쓴다.
here="$(cd "$(dirname "$0")" && pwd)"
exec bash "$here/../_lib/scaffold.sh" "$here/../f3-closeout"
