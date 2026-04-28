from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Reliability Analysis MVP"
    database_url: str = "sqlite:///./reliability.db"


settings = Settings()
