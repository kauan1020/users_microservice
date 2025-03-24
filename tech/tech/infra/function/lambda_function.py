import json
import os
import boto3
import hmac
import hashlib
import base64
import psycopg2
import jwt  # Instale com `pip install PyJWT`
from datetime import datetime, timedelta

# Configurações do Banco de Dados no RDS
DB_HOST = "techdatabase.cxpkgzr59ec4.us-east-1.rds.amazonaws.com"
DB_NAME = "techdatabase"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

# Configurações do JWT
SECRET_KEY = os.getenv("JWT_SECRET", "chave_super_secreta")
ALGORITHM = "HS256"

# Configurações do Cognito
USER_POOL_ID = "us-east-1_TWNF3CSex"
CLIENT_ID = "5ot4obr679k4rogta0j3gik5u4"
CLIENT_SECRET = "123fuhh8ussok7n0n0f78c6b32cnelr7trrn9fm7pgt713vnlffd"


def get_secret_hash(username, client_id, client_secret):
    msg = username + client_id
    dig = hmac.new(client_secret.encode('utf-8'), msg=msg.encode('utf-8'), digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()


def get_user_by_cpf(cpf):
    """Consulta o CPF na tabela `users` do banco PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM users WHERE cpf = %s", (cpf,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2]
            }
        return None
    except Exception as e:
        print("Erro ao consultar banco:", str(e))
        return None


def generate_jwt(user_data):
    """Gera um JWT contendo as informações do usuário"""
    expiration_time = datetime.utcnow() + timedelta(hours=2)
    payload = {
        "sub": user_data["id"],
        "username": user_data["username"],
        "email": user_data["email"],
        "exp": expiration_time
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def lambda_handler(event, context):
    print("Recebendo evento:", json.dumps(event))

    body = json.loads(event.get("body", "{}"))
    cpf = body.get("cpf")
    password = body.get("password")

    if not cpf or not password:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "CPF e senha são obrigatórios"})
        }

    user_data = get_user_by_cpf(cpf)

    if not user_data:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Usuário não encontrado"})
        }

    client = boto3.client("cognito-idp", region_name="us-east-1")
    auth_params = {"USERNAME": cpf, "PASSWORD": password}

    if CLIENT_SECRET:
        auth_params["SECRET_HASH"] = get_secret_hash(cpf, CLIENT_ID, CLIENT_SECRET)

    try:
        response = client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters=auth_params,
            ClientId=CLIENT_ID
        )
        auth_result = response.get("AuthenticationResult")

        if not auth_result:
            return {
                "statusCode": 401,
                "body": json.dumps({"message": "Falha na autenticação"})
            }

        # Gera um JWT próprio baseado nos dados do cliente do banco
        jwt_token = generate_jwt(user_data)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "token": jwt_token,
                "expires_in": 7200
            })
        }
    except client.exceptions.NotAuthorizedException as e:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": str(e)})
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": str(e)})
        }
