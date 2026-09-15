from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from fastapi.responses import RedirectResponse
from routes import login, register, chat
from routes.api import api_login,api_ingest
from db.db_engine import Session, get_db, AsyncSession, engine, Base
from services.document_processor import create_index_if_not_exists
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_index_if_not_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Database tables created successfully.")
    yield
    await engine.dispose()
app = FastAPI(lifespan=lifespan)

@app.get("/")
def first_func():
    return RedirectResponse("/login")

app.include_router(login.router)
app.include_router(register.router)
app.include_router(api_login.router)
app.include_router(chat.router)
app.include_router(api_ingest.router)


if __name__=="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
