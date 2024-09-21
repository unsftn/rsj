from rest_framework.exceptions import APIException


class OptimisticLock(APIException):
    status_code = 409
    default_detail = 'Одредница је у међувремену мењана. Освежите приказ!'
    default_code = 'optimistic_lock'


