from os import environ
from typing import Type, TypeVar, Dict
from pydantic import BaseModel, Field, field_validator

env: Dict[str, str] = dict(environ)
T = TypeVar("T", bound=BaseModel)


def load_config(model: Type[T]) -> T:
    return model(**env)


class SecretConfig(BaseModel):
    allowed_hosts: list[str] = Field(alias="APP_ALLOWED_HOSTS", default_factory=list)
    config_secret_key: str = Field(alias="APP_CONFIG_ENCRYPTION_KEY")
    log_level: str = Field(alias="APP_LOG_LEVEL", default="info")
    pepper: str = Field(alias="APP_PEPPER")

    @field_validator("allowed_hosts", mode="before")
    @classmethod
    def split_allowed_hosts(cls, value):
        if isinstance(value, str):
            return [] if value == "" else value.split(",")
        return value


class RabbitMQConfig(BaseModel):
    host: str = Field(alias="RABBITMQ_HOST")
    port: int = Field(alias="RABBITMQ_PORT")
    login: str = Field(alias="RABBITMQ_USER")
    password: str = Field(alias="RABBITMQ_PASSWORD")
    vhost: str = Field(alias="RABBITMQ_VHOST")


class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    login: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")


class RedisConfig(BaseModel):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
    db: int = Field(alias="REDIS_SESSIONS_DB")
    password: str = Field(alias="REDIS_PASSWORD")


class Config(BaseModel):
    secret: SecretConfig = Field(default_factory=lambda: load_config(SecretConfig))
    rabbitmq: RabbitMQConfig = Field(default_factory=lambda: load_config(RabbitMQConfig))
    postgres: PostgresConfig = Field(default_factory=lambda: load_config(PostgresConfig))
    redis: RedisConfig = Field(default_factory=lambda: load_config(RedisConfig))
