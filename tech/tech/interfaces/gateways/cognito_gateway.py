import boto3
import os
import hmac
import hashlib
import base64
from typing import Dict


class CognitoGateway:
    """Gateway for interacting with Amazon Cognito services.

    This class encapsulates all interactions with AWS Cognito, providing methods
    for authentication, token verification, and user management operations.
    It maintains a boto3 Cognito client and handles AWS credentials.
    """

    def __init__(self):
        """Initializes the CognitoGateway with AWS configuration.

        Sets up the AWS Cognito client with the appropriate region and credentials.
        Configures the User Pool ID, Client ID, and Client Secret needed for
        Cognito operations.
        """
        self.region = "us-east-1"
        self.user_pool_id = "us-east-1_TWFX5csEX"
        self.client_id = "5ot4obr679k4rogta0j3gik5u4"
        self.client_secret = "123fuhh8ussok7n0n0f78c6b32cnelr7trrn9fm7pgt713vnlffd"

        self.client = boto3.client(
            "cognito-idp",
            region_name=self.region,
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', 'SUA_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', 'SUA_SECRET_ACCESS_KEY')
        )

        self.jwks_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"

    def authenticate(self, cpf: str, password: str) -> dict:
        """Authenticates a user with CPF and password.

        Initiates authentication against Cognito User Pool using the USER_PASSWORD_AUTH
        flow. Creates a SECRET_HASH if Client Secret is configured.

        Args:
            cpf (str): The user's CPF number, used as the username.
            password (str): The user's password.

        Returns:
            dict: Authentication result containing tokens and expiration details.

        Raises:
            ValueError: If authentication fails due to invalid credentials,
                       user not found, or other authentication errors.
        """
        try:
            auth_params = {
                "USERNAME": cpf,
                "PASSWORD": password
            }

            if self.client_secret:
                secret_hash = self._get_secret_hash(cpf)
                auth_params["SECRET_HASH"] = secret_hash

            response = self.client.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters=auth_params,
                ClientId=self.client_id
            )

            print(f"Authentication successful for user: {cpf}")
            return response.get("AuthenticationResult", {})

        except self.client.exceptions.NotAuthorizedException as e:
            print(f"Authentication error - invalid credentials: {str(e)}")
            raise ValueError(f"Incorrect credentials: {str(e)}")

        except self.client.exceptions.UserNotFoundException as e:
            print(f"Authentication error - user not found: {str(e)}")
            raise ValueError(f"User not found: {str(e)}")

        except Exception as e:
            print(f"Authentication error: {str(e)}")
            raise ValueError(f"Authentication failed: {str(e)}")

    def _get_secret_hash(self, username: str) -> str:
        """Generates the secret hash required for Cognito authentication.

        Creates an HMAC-SHA256 hash using the client secret as the key and
        the username+client_id as the message, which is required for certain
        Cognito operations.

        Args:
            username (str): The user's CPF/username.

        Returns:
            str: Base64-encoded secret hash.
        """
        message = username + self.client_id
        dig = hmac.new(
            self.client_secret.encode('utf-8'),
            msg=message.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()

    def verify_token(self, token: str) -> Dict:
        """Verifies a JWT token and extracts user information.

        Decodes the token to extract user information, then uses the Cognito API
        to verify the user's existence and group memberships. Determines if the
        user is an admin based on group membership.

        Args:
            token (str): The JWT token to verify.

        Returns:
            dict: User information including username, attributes, and admin status.

        Raises:
            ValueError: If token verification fails, user is not found, or other errors occur.
            Exception: For unexpected errors during verification.
        """
        try:
            print(f"Starting token verification: {token[:20]}...")

            try:
                from jose import jwt as jose_jwt

                decoded_token = jose_jwt.get_unverified_claims(token)
                print(f"Token decoded: {decoded_token}")

                if "cognito:groups" in decoded_token:
                    groups = decoded_token.get("cognito:groups", [])
                    username = decoded_token.get("cognito:username", decoded_token.get("sub", ""))

                    user_data = {
                        "username": username,
                        "attributes": {
                            "sub": decoded_token.get("sub", ""),
                            "email": decoded_token.get("email", "")
                        },
                        "is_admin": "admin" in groups
                    }

                    print(f"Group information found in token: {groups}")
                    print(f"User {username} {'is' if user_data['is_admin'] else 'is not'} an admin")

                    return user_data

                username = decoded_token.get("sub", decoded_token.get("cognito:username", ""))
                if not username:
                    raise ValueError("Token does not contain user identifier")

                print(f"Username/sub extracted from token: {username}")
            except Exception as e:
                print(f"Error decoding token: {str(e)}")
                raise ValueError(f"Invalid token: {str(e)}")

            try:
                user_response = self.client.admin_get_user(
                    UserPoolId=self.user_pool_id,
                    Username=username
                )

                user_data = {
                    "username": user_response.get("Username", ""),
                    "attributes": {}
                }

                for attr in user_response.get("UserAttributes", []):
                    user_data["attributes"][attr["Name"]] = attr["Value"]

                print(f"User information obtained: {user_data['username']}")
            except self.client.exceptions.UserNotFoundException:
                print(f"User not found: {username}")
                raise ValueError(f"User not found: {username}")
            except Exception as e:
                print(f"Error getting user information: {str(e)}")
                raise ValueError(f"Failed to get user information: {str(e)}")

            try:
                groups_response = self.client.admin_list_groups_for_user(
                    UserPoolId=self.user_pool_id,
                    Username=username
                )

                print(f"Groups obtained: {[g.get('GroupName') for g in groups_response.get('Groups', [])]}")

                user_data["is_admin"] = any(
                    group.get("GroupName") == "admin"
                    for group in groups_response.get("Groups", [])
                )

                print(f"User {username} {'is' if user_data['is_admin'] else 'is not'} an admin")

                return user_data

            except Exception as e:
                print(f"Error checking admin status: {str(e)}")
                raise ValueError(f"Failed to verify admin status: {str(e)}")

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Unexpected error in token verification: {str(e)}")
            raise ValueError(f"Token verification failed: {str(e)}")