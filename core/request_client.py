import requests
import json
from common import log


class RequestClient:

    def __init__(self, api_host):
        self.api_host = api_host
        self.session = requests.session()

    def get(self, path, **kwargs):
        response = self.request(path, "GET", **kwargs)
        return response

    def post(self, path, data=None, json_data=None, **kwargs):
        response = self.request(path, "POST", data, json_data, **kwargs)
        return response

    def put(self, path, data=None, **kwargs):
        response = self.request(path, "PUT", data, **kwargs)
        return response

    def delete(self, path, **kwargs):
        response = self.request(path, "DELETE", **kwargs)
        return response

    def patch(self, path, data=None, **kwargs):
        response = self.request(path, "PATCH", data, **kwargs)
        return response

    def request(self, path, method, data=None, json_data=None, **kwargs):
        url = f"https://{self.api_host + path}"
        method = method.upper()
        headers = kwargs.get("headers")
        params = kwargs.get("params")
        files = kwargs.get("files")
        cookies = kwargs.get("cookies")
        self.request_log(url, method, data, json_data, params, files, cookies)
        if method == "GET":
            return self.session.get(url, **kwargs)
        if method == "POST":
            return requests.post(url, data, json_data, **kwargs)
        if method == "PUT":
            if json_data:
                # PUT 和 PATCH 中没有提供直接使用json参数的方法，因此需要用data来传入
                data = json.dumps(json_data)
            return self.session.put(url, data, **kwargs)
        if method == "DELETE":
            return self.session.delete(url, **kwargs)
        if method == "PATCH":
            if json_data:
                data = json.dumps(json_data)
            return self.session.patch(url, json_data, **kwargs)

    def request_log(self, url, method, data=None, json_data=None, params=None, files=None, cookies=None,
                    **kwargs):
        log.info(f"接口请求地址 ==>> {url}")
        log.info(f"接口请求方式 ==>> {method}")
        # Python3中，json在做dumps操作时，会将中文转换成unicode编码，因此设置 ensure_ascii=False
        log.info(f"接口请求头 ==>> {self.session.headers}")
        log.info(f"接口请求 params 参数 ==>> {json.dumps(params, indent=4, ensure_ascii=False)}")
        log.info(f"接口请求体 data 参数 ==>> {json.dumps(data, indent=4, ensure_ascii=False)}")
        log.info(f"接口请求体 json 参数 ==>> {json.dumps(json_data, indent=4, ensure_ascii=False)}")
        log.info(f"接口上传附件 files 参数 ==>> {files}")
        log.info(f"接口 cookies 参数 ==>> {json.dumps(cookies, indent=4, ensure_ascii=False)}")
