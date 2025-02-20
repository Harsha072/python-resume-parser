from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
import os

#Get the absolute path to the .env file
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)  # Explicitly load the .env file

class Settings(BaseSettings):
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_username: str
    rabbitmq_password: str
    rabbitmq_queue: str
    feedback_queue: str  # Ensure this exists in .env

    class Config:
        env_file = str(env_path)  #Explicitly set the .env file path

# Initialize settings
settings = Settings()

# Debug output to ensure 'feedback_queue' is loaded
print(f"Feedback Queue: {settings.feedback_queue}")
