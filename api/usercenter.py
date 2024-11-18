from core import RequestClient
from config import api_host


class Usercenter(RequestClient):
    def __init__(self):
        super(Usercenter, self).__init__(api_host)
        self.base_path = "/api/homework"
        self.session.headers = {
            "Host": self.api_host,
            "XC-App-User-SchoolId": '6',
            "AuthToken": f"d416f111-1690-49f0-843a-6c6a5d866359"
        }

    def get_school_courses(self, **kwargs):
        path = "/api/usercenter/common/school/course/list"
        request = self.get(path, **kwargs)
        return request

    def my_suggestions_using_get(self, **kwargs):
        path = "/api/usercenter/common/loginuserinfo/suggestion"
        method = "POST"
        request = self.request(path, method, **kwargs)
        return request
