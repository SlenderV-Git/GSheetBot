from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f'.env',
        env_file_encoding='utf-8',
    )

    API_TOKEN : str
    GOOGLE_SHEET_ID : str
    CREDENTIALS_FILE : str

def get_settings() -> Settings:
    return Settings()