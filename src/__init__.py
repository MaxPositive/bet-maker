from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.config import settings

from src.bets.routers import router as bets_router

from src.pkgs.db.engine import sessionmanager

DATABASE_URL = settings.DATABASE_URL


def init_app(init_db=True) -> FastAPI:
    lifespan = None

    if init_db:
        sessionmanager.init(DATABASE_URL)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        if sessionmanager._engine is not None:
            await sessionmanager.close()

    app = FastAPI(lifespan=lifespan)

    app.include_router(bets_router)

    return app
