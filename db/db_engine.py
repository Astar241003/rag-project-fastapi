import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
load_dotenv()

db_url = os.environ.get("db_url")
engine=create_async_engine(url=db_url)

Session = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with Session() as session:
        yield session
