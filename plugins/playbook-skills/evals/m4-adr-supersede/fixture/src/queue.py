# 작업 큐. 현재 Redis List.
import redis

client = redis.Redis()


def enqueue(job):
    client.rpush("jobs", job)
