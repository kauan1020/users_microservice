import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from tech.core.domain.models import User, table_registry


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    table_registry.metadata.drop_all(engine)


def test_should_create_user(session):
    user = User(
        username='kauan',
        email='kauan@fiap.com',
        password='senhas',
        cpf='42190223489',
    )
    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'kauan@fiap.com'))

    assert result.username == 'kauan'
