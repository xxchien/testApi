from api import AutoApi
from core import RequestResponse
from common import log


def auto_get_response(module: str, operation_id: str, **kwargs):
    """
    请求接口
    :param module:
    :param operation_id:
    :return:
    """
    try:
        auto_api = AutoApi(module)
        request = auto_api.auto_request(operation_id, **kwargs)
        response = RequestResponse(request).data_pyob
        return response
    except Exception as e:  # 捕获异常
        log.error(f"请求时发生异常: {str(e)}")
        return None


if __name__ == '__main__':
    result = auto_get_response('usercenter', 'listCoursesUsingGET')
    print(result)
