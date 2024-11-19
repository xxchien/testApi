import json
from common import log


class RequestResponse:
    def __init__(self, request):
        self.response = request

        self.status_code = self.response.status_code

        self.data_bytes = self.response.content

        self.data_str = self.data_bytes.decode('utf-8')

        self.data_pyob = json.loads(self.data_str)

        self.data_json = json.dumps(self.data_pyob)

        self.data_dict = self.data_pyob
