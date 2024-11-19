from core import RequestClient
from config import *
from common import load_data


class AutoApi(RequestClient):
    def __init__(self, module: str):
        """
        :param module: 模块名字
        """
        super(AutoApi, self).__init__(api_host)
        self.module_name = module
        self.docs_path = os.path.join(API_DATA, f"{self.module_name}_api_docs.json")
        self.docs = load_data.load_json(self.docs_path)
        self.base_path = self.docs['basePath']
        self.paths = self.docs['paths']

        self.session.headers = {
            "Host": api_host
        }
        self.session.headers.update(base_headers)

    def get_path_info(self, operation_id):
        # 遍历输入的所有路径及其方法
        for path, methods in self.paths.items():
            for method, details in methods.items():
                details_operation_id = details.get("operationId")
                if details_operation_id == operation_id:
                    path_info = {
                        'operation_id': operation_id,
                        'path': path,
                        'method': method,
                        'details': details
                    }
        return path_info

    def get_headers(self):
        """
        根据path_info来确认headers
        TODO: 想想没有必要之后再做吧
        :return:
        """
        pass

    def auto_request(self, operation_id, **kwargs):
        path_info = self.get_path_info(operation_id)
        path = path_info['path']
        complete_path = f"{self.base_path}{path}"
        method = path_info['method'].upper()
        request = self.request(complete_path, method, **kwargs)
        return request


if __name__ == "__main__":
    # from itertools import islice

    auto = AutoApi('usercenter')
    # my_dict = auto.paths
    # result = dict(islice(my_dict.items(), 2))
    sss = auto.auto_request('listCoursesUsingGET').content.decode('utf-8')
    print(sss)
