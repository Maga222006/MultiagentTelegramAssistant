from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Float

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location = Column(String, nullable=True)

class UserConfig(Base):
    __tablename__ = "user_config"

    user_id = Column(String, primary_key=True, index=True)
    openweathermap_api_key = Column(String, nullable=True)
    github_token = Column(String, nullable=True)
    tavily_api_key = Column(String, nullable=True)
    openai_api_key = Column(String, nullable=True)
    openai_api_base = Column(String, nullable=True)
    model = Column(String, nullable=True)
    image_model = Column(String, nullable=True)
    stt_model = Column(String, nullable=True)