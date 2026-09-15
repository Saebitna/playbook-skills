2026-09-12 장애 회고: 워커 재시작 때 작업 37건 유실. List 는 ack 가 없어 복구 불가.

Redis Streams 로 바꾸기로 했다. consumer group 과 XACK 로 미처리 작업을 재할당할 수 있다.
Kafka 도 봤지만 인프라가 하나 더 늘고 처리량(피크 약 300 job/s)에 비해 과하다.
