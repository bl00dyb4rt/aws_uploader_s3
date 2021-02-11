import json


class CustomResponse:
    @staticmethod
    def response(status='success', data="", message=""):
        success = {
            "status": status,
            "data": data,
            "message": message
        }

        error = {
            "status": status,
            "data": data,
            "message": message
        }
        if status == "success":
            return success
        else:
            return error
