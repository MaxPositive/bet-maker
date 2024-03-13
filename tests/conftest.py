from contextlib import ExitStack

import pytest
import pytest_asyncio

from async_asgi_testclient import TestClient

from src import init_app
from src.config import settings
from src.pkgs.db.engine import get_db, sessionmanager

DATABASE_URL = settings.DATABASE_URL


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(init_db=True)


@pytest_asyncio.fixture()
async def client(app):
    host, port = "0.0.0.0", "9000"
    scope = {"client": (host, port)}
    async with TestClient(app, scope=scope) as c:
        yield c


@pytest.fixture(scope="function", autouse=True)
async def connection():
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


async def get_db_override():
    async with sessionmanager.session() as session:
        yield session


@pytest.fixture(scope="function", autouse=True)
async def session_override(app):

    app.dependency_overrides[get_db] = get_db_override
