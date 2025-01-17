from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tech.infra.settings.settings import Settings

load_dotenv()
engine = create_engine(Settings().DATABASE_URL)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
