from redis import Redis

from app import REDIS_URL


class RedisService:
    """Service to interact with Redis."""

    __client = None
    """Redis client instance."""

    class Namespace:
        """Namespace for Redis keys."""

        TIME = "time"
        """Namespace for time-related keys."""

        STATUS = "status"
        """Namespace for status-related keys."""

    class Status:
        """Status values for Redis keys."""

        ACTIVE = "active"
        """Active status."""

        INACTIVE = "inactive"
        """Inactive status."""

    @staticmethod
    def connect():
        """Connect to Redis."""
        RedisService.__client = Redis.from_url(REDIS_URL)

    @staticmethod
    def get_client():
        """Get Redis client."""
        if RedisService.__client is None:
            RedisService.connect()

        return RedisService.__client

    @staticmethod
    def get(key):
        """Get a value from Redis."""
        return RedisService.get_client().get(key)

    @staticmethod
    def set(key, value):
        """Set a value in Redis."""
        RedisService.get_client().set(key, value)

    @staticmethod
    def setKeyWithNamespace(namespace, key, value):
        """Set a value in Redis with a namespace."""
        RedisService.get_client().set(f"{namespace}:{key}", value)

    @staticmethod
    def getKeyWithNamespace(namespace, key):
        """Get a value from Redis with a namespace."""
        return RedisService.get_client().get(f"{namespace}:{key}")

    @staticmethod
    def set_time(key, value):
        """Set a time-related value in Redis."""
        RedisService.setKeyWithNamespace(RedisService.Namespace.TIME, key, value)

    @staticmethod
    def get_time(key):
        """Get a time-related value from Redis."""
        return RedisService.getKeyWithNamespace(RedisService.Namespace.TIME, key)

    @staticmethod
    def set_status(key, value):
        """Set a status-related value in Redis."""
        RedisService.setKeyWithNamespace(RedisService.Namespace.STATUS, key, value)

    @staticmethod
    def get_status(key):
        """Get a status-related value from Redis."""
        raw = RedisService.getKeyWithNamespace(RedisService.Namespace.STATUS, key)
        return raw.decode("utf-8") if raw else None
