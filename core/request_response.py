import json


class RequestResponse:
    def __init__(self, request):
        self.response = request
        self.status_code = self.response.status_code
        self.data_bytes = self.response.content
        self.data_dict = json.loads(self.data_bytes)
        self.data_str = self.data_bytes.decode('utf-8')
        self.data_json = json.dumps(self.data_dict)
        self.data_code = self.data_dict["code"]
        self.data_data = self.data_dict["data"]