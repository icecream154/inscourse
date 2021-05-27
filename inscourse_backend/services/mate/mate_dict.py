import time

from django.db.models import Q

from inscourse_backend.models.mate.mate import Mate
from inscourse_backend.models.mate.mate_assignment import MateAssignment
from inscourse_backend.models.user import User


def to_mate_dict(mate: Mate, user: User):
    other_user = mate.requester if user == mate.acceptor else mate.acceptor
    curr_date = time.strftime('%Y-%m-%d')
    finished = MateAssignment.objects.filter(Q(mate=mate) & Q(status=3)).count()
    not_finished = MateAssignment.objects.filter(Q(mate=mate) & Q(assignment_date__gte=curr_date) & ~Q(status=3)).count()
    mate_item = {
        'mate_id': mate.mate_id,
        'course': mate.course.name,
        'course_id': mate.course.course_id,
        'mate_username': other_user.username,
        'my_user_id': user.user_id,
        'mate_user_id': other_user.user_id,
        'finished': finished,
        'not_finished': not_finished
    }
    return mate_item
