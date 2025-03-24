import pytest
from fastapi.testclient import TestClient
from tech.api.app import app
from tech.infra.databases.database import get_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from tech.infra.repositories.sql_alchemy_models import table_registry

table_registry

@pytest.fixture
def engine():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    table_registry.metadata.create_all(engine)
    yield engine
    table_registry.metadata.drop_all(engine)

@pytest.fixture
def session(engine):
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture
def client(session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
