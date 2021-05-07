import random
import string


def generate_code_from_id(uid: int, secret: int, salt: int, left: int) -> str:
    code = hex(uid * secret + salt)[2:].upper()
    while len(code) < 6:
        code = '0' + code
    rc1 = _get_random_character()
    rc2 = _get_random_character()
    if (ord(rc1) + ord(rc2)) % 2 != left:
        rc2 = chr(ord(rc2) + 1 if rc2 != 'Z' else ord(rc2) - 1)
    code = code[5] + rc1 + code[3] + code[1] + rc2 + code[0] + code[2] + code[4]
    return code


def decode_id_from_code(code: str, secret: int, salt: int, left: int) -> int:
    if len(code) != 8 or (ord(code[1]) + ord(code[4])) % 2 != left:
        return -1
    origin_hex = '0x' + (code[5] + code[3] + code[6]
                         + code[2] + code[7] + code[0]).lower()
    id_with_secret = int(origin_hex, 16) - salt
    if id_with_secret < 0 or id_with_secret % secret != 0:
        return -1
    return id_with_secret / secret


COURSE_INVITATION_SECRET = 3
COURSE_INVITATION_SALT = 18433


def generate_course_invitation_code(course_id: int) -> str:
    return generate_code_from_id(course_id, COURSE_INVITATION_SECRET, COURSE_INVITATION_SALT, 0)


def decode_course_id_from_code(invitation_code: str) -> int:
    return decode_id_from_code(invitation_code, COURSE_INVITATION_SECRET, COURSE_INVITATION_SALT, 0)


MATE_INVITATION_SECRET = 5
MATE_INVITATION_SALT = 9601


def generate_mate_invitation_code(mate_invitation_id: int) -> str:
    return generate_code_from_id(mate_invitation_id, MATE_INVITATION_SECRET, MATE_INVITATION_SALT, 1)


def decode_mate_invitation_id_from_code(invitation_code: str) -> int:
    return decode_id_from_code(invitation_code, MATE_INVITATION_SECRET, MATE_INVITATION_SALT, 1)


def _get_random_character():
    return random.choice(string.ascii_uppercase)
