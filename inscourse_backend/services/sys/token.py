import time

from inscourse_backend.models.user import User


token_dict = {}
# default expire time set to 10800 seconds (3 hour)
_EXPIRE_TIME = 10800
TOKEN_HEADER_KEY = 'HTTP_TOKEN'


def _get_token_by_id(token_dictionary: {str: (User, float)}, user_id: int):
    return [k for k, v in token_dictionary.items() if v[0].user_id == user_id]


def _generate_token_string(user: User):
    return "fakeToken" + str(user.openid)


def update_token(user: User):
    token_by_id = _get_token_by_id(token_dict, user.user_id)
    if len(token_by_id) == 1:
        del token_dict[token_by_id[0]]

    new_token = _generate_token_string(user)
    new_expire_time = time.time() + _EXPIRE_TIME
    token_dict[new_token] = (user, new_expire_time)
    return new_token, new_expire_time


def fetch_user_by_token(token: str):
    try:
        user, expire_time = token_dict[token]
        if time.time() > expire_time:
            del token_dict[token]
            return None
        return user
    except KeyError:
        return None


def expire_token(token: str):
    if token in token_dict:
        del token_dict[token]
