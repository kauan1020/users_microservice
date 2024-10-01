from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from tech.adapters.driven.infra.database import get_session
from tech.core.domain.models import User
from tech.core.domain.schemas import UserPublic, UserSchema, UserList, Message
from tech.core.domain.security import get_password_hash, get_cpf_hash

router = APIRouter()


@router.post('/', response_model=UserPublic, status_code=201)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    if len(user.cpf) != 11 or not user.cpf.isdigit():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='CPF must contain exactly 11 digits and be numeric.',
        )

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username)
            | (User.email == user.email)
            | (User.cpf == user.cpf)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )
        elif db_user.cpf == user.cpf:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='CPF already exists',
            )

    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        cpf=user.cpf,
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def read_users(
    limit: int = 10, skip: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).limit(limit).offset(skip)).all()
    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    db_user.username = user.username
    db_user.password = get_password_hash(user.password)
    db_user.email = user.email
    db_user.cpf = get_cpf_hash(user.cpf)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    session.delete(db_user)
    session.commit()
    return {'message': 'User deleted'}
