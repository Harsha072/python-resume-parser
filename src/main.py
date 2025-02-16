from messaging.consumer import start_consumer

# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     rabbitmq_host: str
#     rabbitmq_port: int
#     rabbitmq_username: str
#     rabbitmq_password: str
#     rabbitmq_queue: str

#     class Config:
#         # Specify the relative path to the .env file
#         env_file = "../.env"  # One level up to access the .env file

# # Create an instance of Settings
# settings = Settings()
# print(settings)

if __name__ == "__main__":
    start_consumer()
    print("starting consumer")