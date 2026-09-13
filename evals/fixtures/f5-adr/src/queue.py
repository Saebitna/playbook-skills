# 작업 큐 백엔드. 현재 Redis 사용.
import redis

client = redis.Redis()


def enqueue(job):
    client.rpush("jobs", job)
