작업 큐 백엔드 후보를 놓고 검토했다.

- Postgres SKIP LOCKED: 인프라 추가 없음. 처리량 한계 약 2k/s.
- Redis Streams: 처리량 충분. 인프라 1개 추가. 영속성 설정 필요.
- SQS: 운영 부담 없음. 지연 크고 로컬 개발 불편. 벤더 종속.

Redis Streams 로 간다. 현재 피크가 5k/s 라 Postgres 는 탈락,
로컬 개발 편의 때문에 SQS 도 탈락.
