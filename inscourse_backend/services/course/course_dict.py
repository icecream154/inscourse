from inscourse_backend.models.course.course import Course
from inscourse_backend.models.course.course_join import CourseJoin
from inscourse_backend.models.user import User


def is_joined(user: User, course: Course):
    try:
        CourseJoin.objects.get(user=user, course=course)
        return True
    except CourseJoin.DoesNotExist:
        return False


def to_course_dict(course: Course, user: User):
    dic = course.to_dict()
    dic['is_joined'] = is_joined(user, course)
    return dic
