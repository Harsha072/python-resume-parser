from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
import os

# Get the absolute path to the .env file
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)

class Settings(BaseSettings):
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_username: str
    rabbitmq_password: str
    rabbitmq_queue: str
    feedback_queue: str

    class Config:
        env_file = env_path  # Optional, since we're using load_dotenv

settings = Settings()
print(settings)