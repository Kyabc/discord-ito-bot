from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DISCORD_TOKEN: str
    OWNER_ID: str
    LOG_DIR: str

    model_config = ConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )


settings = Settings()

if __name__ == "__main__":
    print(settings)
