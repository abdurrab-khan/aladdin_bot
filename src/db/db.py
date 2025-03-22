class RedisDB:
    def __init__(self):
        self.RADIS_HOST = 'localhost'
        self.RADIS_PORT = 6379

    def connect(self):
        """
        Connect to redis database
        """
        pass

    def disconnect(self):
        """
        Disconnect from redis database
        """
        pass

    def get(self, key:str) -> str:
        """
        Get the value from redis database
        """
        pass

    def set(self, key:str, value:str) -> None:
        """
        Set the value in redis database
        """
        pass

    def delete(self, key:str) -> None:
        """
        Delete the value from redis database
        """
        pass