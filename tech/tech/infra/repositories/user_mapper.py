from tech.domain.entities.users import User
from tech.infra.repositories.sql_alchemy_models  import SQLAlchemyUser
from tech.domain.value_objects import CPF

class UserMapper:
    @staticmethod
    def to_persistence(user: User) -> SQLAlchemyUser:
        return SQLAlchemyUser(
            id=user.id,
            username=user.username,
            password=user.password,
            cpf=str(user.cpf),
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    @staticmethod
    def to_domain(sqlalchemy_user: SQLAlchemyUser) -> User:
        user = User(
            username=sqlalchemy_user.username,
            password=sqlalchemy_user.password,
            cpf=CPF(sqlalchemy_user.cpf),
            email=sqlalchemy_user.email
        )
        user.id = sqlalchemy_user.id
        user.created_at = sqlalchemy_user.created_at
        user.updated_at = sqlalchemy_user.updated_at
        return user
