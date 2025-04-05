from redis import Redis
from redis.exceptions import ConnectionError, RedisError, MaxConnectionsError
from dotenv import load_dotenv
from os import getenv
from typing import Optional


def redis_call(func):
    def wrapper(self, * args, **kwargs):
        if not self.client:
            print("Redis client is not connected.")
            return None

        try:
            return func(self, *args, **kwargs)
        except RedisError as e:
            print(f"Redis error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    return wrapper


class RedisDB:
    def __init__(self):
        load_dotenv()
        self.host = getenv("REDIS_HOST")
        self.port = getenv("REDIS_PORT")
        self.password = getenv("REDIS_PASSWORD")
        self.username = "default"
        self.db = 0
        self.client = None

    def connect(self):
        """
        Connect to redis database
        """
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
            print("Redis connected successfully.")

            self.pool = self.client.connection_pool

            return True
        except ConnectionError as e:
            print(f"Redis connection error: {e}")
            return False
        except RedisError as e:
            print(f"Redis error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
        except MaxConnectionsError as e:
            print(f"Max connection hit error: {e}")
            return False

    def disconnect(self):
        """
        Disconnect from redis database
        """
        try:
            if self.client:
                self.pool.disconnect()
                self.client = None
                self.pool = None

                print("Redis disconnected successfully.")
                return True
        except Exception as e:
            print(f"Error during Redis disconnect: {e}")
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
    def get_all_member(self, key):
        """
        Get all members of the set stored at key.

        args:
            key (str): The key of the set.

        return:
            list: A list of all members of the set.
        """
        return list(self.client.smembers(key))

    @redis_call
    def add_to_set(self, key: str, member: str, expire_time: Optional[int] = None) -> int:
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
        if expire_time:
            return self.client.sadd(
                key,
                member,
                {
                    "EX": expire_time,
                }
            )
        else:
            return self.client.sadd(key, member)

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
