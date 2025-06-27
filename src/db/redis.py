from os import getenv
from redis import Redis
from typing import Optional
from logging import warning, error, info
from redis.exceptions import ConnectionError, RedisError, MaxConnectionsError

from ..constants.redis_key import PRODUCT_URL_CACHE_KEY


def redis_call(func):
    def wrapper(self, * args, **kwargs):
        if not self.client:
            warning("⚠️ Redis client is not connected.")
            return None

        try:
            return func(self, *args, **kwargs)
        except RedisError as e:
            error(f"⛔ Redis error: {e}")
            return None
        except Exception as e:
            error(f"⛔ Unexpected error: {e}")
            return None

    return wrapper


class RedisDB:
    def __init__(self):
        self.host = getenv("REDIS_HOST")
        self.port = getenv("REDIS_PORT")
        self.password = getenv("REDIS_PASSWORD")
        self.username = "default"
        self.db = 0
        self.client = None
        self.pool = None

    def __enter__(self):
        try:
            self.client = Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                username=self.username,
                db=self.db,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=2,
                health_check_interval=30
            )

            self.client.ping()
            info("🔗 Redis connected successfully.")

            self.pool = self.client.connection_pool

            return self
        except ConnectionError as e:
            error(f"⛔ Redis connection error: {e}")
            return False
        except RedisError as e:
            error(f"⛔ Redis error: {e}")
            return False
        except Exception as e:
            error(f"⛔ Unexpected error: {e}")
            return False
        except MaxConnectionsError as e:
            warning(f"⚠️ Max connection hit error: {e}")
            return False

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if self.client:
                self.pool.disconnect()
                self.client = None
                self.pool = None
                info("🔒 Redis disconnected successfully.")
                return True
        except Exception as e:
            error(f"⛔ Error during Redis disconnect: {e}")
            return False

        if exc_type:
            error(
                f"⛔ An error occurred while disconnecting the db: {exc_value}")
            return False

        return True

    @redis_call
    def is_member(self, key: str, member: str,) -> bool | None:
        """
        Check if the given value is a member of the set stored at key.

        args:
            key (str): The key of the set.
            member (str): The value to check.

        return:
            bool: True if the value is a member of the set, False otherwise.
        """
        if self.client.sismember(key, member):
            return True
        else:
            return False

    @redis_call
    def get_all_member(self, key) -> list:
        """
        Get all members of the set stored at key.

        args:
            key (str): The key of the set.

        return:
            list: A list of all members of the set.
        """
        return list(self.client.smembers(key))

    @redis_call
    def add_to_set(self, key: str, member: str | list, expire_time: Optional[int] = None) -> int:
        """
        Set the value in redis database and store it in a set.

        args:
            key (str): The key to set.
            member (str): The value to set.
            expire_time (int): The expiration time in seconds.
                If not provided, the value will not expire.

        return:
            None
        """
        member = [member] if isinstance(member, str) else member
        result = self.client.sadd(key, *member)

        if expire_time:
            self.client.expire(key, expire_time)

        return result

    @redis_call
    def remove_to_set(self, key: str, member: str) -> int:
        """
        Remove the giver member from the set stored at key.

        args:
            key (str): The key of the set.
            member (str): The member to remove.

        return:
            None
        """
        return self.client.srem(key, member)

    @redis_call
    def remove_set(self, key: str) -> int:
        """
        Remove the set stored at key.

        args:
            key (str): The key of the set.

        return:
            None
        """
        return self.client.delete(key)

    @redis_call
    def is_url_cached(self, url: str, pattern: str = f"{PRODUCT_URL_CACHE_KEY}*") -> bool:
        """
        Check if the given URL is already in the Redis database.

        args:
            url (str): The URL to check.
            pattern (str): The pattern to match keys.
                Default is PRODUCT_URL_CACHE_KEY.

        return:
            bool: True if the URL is found, False otherwise.
        """
        cursor = 0

        while True:
            cursor, keys = self.client.scan(cursor=cursor, match=pattern)

            if not keys:
                if cursor == 0:
                    break
                continue

            pipe = self.client.pipeline()
            for key in keys:
                pipe.sismember(key, url)

            results = pipe.execute()
            if any(results):
                return True

            if cursor == 0:
                break

        return False
