from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
import os
from dotenv import load_dotenv
from .models import Base

load_dotenv()

engine = create_async_engine(os.getenv('DB_URL'),echo=True,pool_pre_ping=True,pool_size=10,max_overflow=5)

async_session_factory = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False,
    class_=AsyncSession
)

async def init_models():

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)