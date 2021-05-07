from inscourse_backend.utils.invitation_code_generator import *

if __name__ == '__main__':
    for i in range(100):
        code = generate_course_invitation_code(i)
        print('code for %d: %s and decoded result %d' % (i, code, decode_course_id_from_code(code)))

    for i in range(100):
        code = generate_mate_invitation_code(i + 2333)
        print('code for %d: %s and decoded result %d' % (i + 2333, code, decode_mate_invitation_id_from_code(code)))
