from rest_framework.exceptions import APIException


class ItemsNotFound(APIException):
    status_code = 404
    default_detail = 'Products not found'
    default_code = 'Not Found'


class BadRequest(APIException):
    status_code = 400
    default_detail = 'Data format is wrong'
    default_code = 'Bad Request'
