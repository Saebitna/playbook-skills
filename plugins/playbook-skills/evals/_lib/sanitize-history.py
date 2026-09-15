#!/usr/bin/env python3
"""eval 실행에서 얻은 Claude Code 세션 트랜스크립트를 history_file 용으로 정리한다.

    python3 _lib/sanitize-history.py <원본 세션 .jsonl> <케이스>/history.jsonl

- user / assistant 메시지만 남기고 parentUuid 를 순서대로 다시 잇는다.
  첨부(샌드박스 설정, 환경 경로), 파일 스냅샷 같은 항목은 버린다.
- 임시 워크스페이스·홈 경로와 현재 사용자 이름을 중립 값으로 바꾼다.

저장소에 커밋되는 파일이다. 결과를 반드시 한 번 더 검색해 개인 정보가 없는지 확인한다.
"""
import json
import os
import re
import sys

KEEP_KEYS = {"type", "message", "uuid", "parentUuid", "isSidechain", "userType",
             "sessionId", "timestamp", "version", "sourceToolAssistantUUID", "isMeta"}

SCRUB = [
    (re.compile(r"/private/tmp/e-[A-Za-z0-9]+/home/cwd"), "/workspace"),
    (re.compile(r"/private/tmp/e-[A-Za-z0-9]+"), "/sandbox"),
    (re.compile(r"/private/tmp/claude-[0-9]+/[^\s\"']*"), "/scratch"),
    (re.compile(r"/Users/[A-Za-z0-9._-]+"), "/home/user"),
    (re.compile(r"\b" + re.escape(os.environ.get("USER", "nobody")) + r"\b"), "user"),
]


def scrub(text):
    for pattern, replacement in SCRUB:
        text = pattern.sub(replacement, text)
    return text


def main(src, dst):
    kept, prev = [], None
    for line in open(src):
        entry = json.loads(line)
        if entry.get("type") not in ("user", "assistant"):
            continue
        entry = {k: v for k, v in entry.items() if k in KEEP_KEYS}
        entry["parentUuid"] = prev
        entry["sessionId"] = "00000000-0000-0000-0000-000000000000"
        prev = entry["uuid"]
        kept.append(json.loads(scrub(json.dumps(entry, ensure_ascii=False))))
    with open(dst, "w") as f:
        for entry in kept:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"{dst}: {len(kept)} entries")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
