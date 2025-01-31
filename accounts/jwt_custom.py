from rest_framework_jwt.settings import api_settings
from calendar import timegm
from datetime import datetime


def jwt_payload_handler(user):
    payload = {
        'username': user.username,
    }

    issued_at = datetime.utcnow()
    expires_at = issued_at + api_settings.JWT_EXPIRATION_DELTA

    payload['iat'] = timegm(issued_at.utctimetuple())
    payload['exp'] = timegm(expires_at.utctimetuple())

    return payload


def jwt_get_username_from_payload(payload):
    return payload.get("username")


def jwt_response_payload_handler(token, user=None, request=None):
    if user.usertype.id == 4:
        return{
            'token': token,
        }
    return {
        'token': token,
    }