from pydantic import BaseSettings

class Settings(BaseSettings):
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_username: str
    rabbitmq_password: str
    rabbitmq_queue: str

    class Config:
        env_file = ".env"

settings = Settings()