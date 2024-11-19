from core import RequestClient
from config import *


class Usercenter(RequestClient):
    def __init__(self):
        super(Usercenter, self).__init__(api_host)
        self.base_path = "/api/homework"
        self.session.headers = {
            "Host": api_host
        }
        self.session.headers.update(base_headers)

    def get_school_courses(self, **kwargs):
        path = "/api/usercenter/common/school/course/list"
        request = self.get(path, **kwargs)
        return request

    def my_suggestions_using_get(self, **kwargs):
        path = "/api/usercenter/common/loginuserinfo/suggestion"
        method = "POST"
        request = self.request(path, method, **kwargs)
        return request
