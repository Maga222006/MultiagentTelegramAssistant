from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from database.models import UserConfig, Base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
import os

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_config_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_or_update_config(user_id: str, **kwargs):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            config = await session.get(UserConfig, user_id)
            if config:
                for key, value in kwargs.items():
                    if hasattr(config, key) and value:
                        setattr(config, key, value)
            else:
                config = UserConfig(user_id=user_id, **kwargs)
                session.add(config)
        await session.commit()

async def get_config_by_user_id(user_id: str):
    async with AsyncSessionLocal() as session:
        config = await session.get(UserConfig, user_id)
        if config:
            return {key: getattr(config, key) for key in config.__table__.columns.keys()}
        return None

async def load_config_to_env(user_id: str):
    config = await get_config_by_user_id(user_id)
    if not config:
        return

    for key, value in config.items():
        if value is not None:
            env_key = key.upper()
            os.environ[env_key] = value
