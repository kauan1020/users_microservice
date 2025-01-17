from datetime import datetime
from typing import Optional
from tech.domain.value_objects import CPF

class User:
    def __init__(self, username: str, password: str, cpf: CPF, email: str, id: Optional[int] = None):
        self.id = id
        self.username = username
        self.password = password
        self.cpf = cpf
        self.email = email
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update_password(self, new_password: str):
        self.password = new_password
        self.updated_at = datetime.now()

    def update_email(self, new_email: str):
        self.email = new_email
        self.updated_at = datetime.now()