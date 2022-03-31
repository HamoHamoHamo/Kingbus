from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import jwt #import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

User=get_user_model()

@database_sync_to_async
def get_user(username):
    return User.objects.get(username=username)


# https://morioh.com/p/71b218237c9d
class TokenAuthMiddleware:
    """
    Custom token auth middleware
    """
 
    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner
 
    async def __call__(self, scope, receive, send):
 
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()
        # Get the token
        # token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

        #https://stackoverflow.com/questions/56907779/passing-headers-to-django-channels-using-javascript-websockets-to-authenticate-u
        # headers = dict(scope['headers'])
        # print(headers)
        token_name, token = dict(scope['headers'])[b'authorization'].decode().split()
        #token = headers[b'authorization']
        print(token)
        
        # # Try to authenticate the user
        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            # Token is invalid
            print(e)
            return None
        else:
            #  Then token is valid, decode it
            decoded_data = jwt.decode(token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=["HS256"])
            print(decoded_data)
        # Will return a dictionary like -
        # {
        #     "token_type": "access",
        #     "exp": 1568770772,
        #     "jti": "5c15e80d65b04c20ad34d77b6703251b",
        #     "user_id": 6
        # }
        
        # Get the user using ID
        scope['user'] = await get_user(decoded_data["username"])
 
        # Return the inner application directly and let it run everything else
        # return self.inner(dict(scope, user=user))
        # return decoded_data['username'] 
        return await self.inner(scope, receive, send)