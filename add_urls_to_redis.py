import config
import redis


# cli = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
cli = redis.StrictRedis.from_url(config.REDIS_URI, decode_responses=True)
with open("urls.txt") as f:
    text = f.read()
    urls = []
    for url in text.strip().split("\n"):
        urls.append(url.strip())

    cli.lpush(config.ASR_AUDIO_URL_LIST, *urls)
