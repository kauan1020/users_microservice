from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_cpf_hash(cpf: str):
    return pwd_context.hash(cpf)


def verify_cpf(plain_cpf: str, hashed_cpf: str):
    return pwd_context.verify(plain_cpf, hashed_cpf)
