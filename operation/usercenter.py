from api import Usercenter
from common import log
from core import RequestResponse

user_center = Usercenter()


def get_school_courses():
    """
    获取学校课程
    :return:
    """
    try:
        request = user_center.get_school_courses()  # 修正拼写错误：requeset -> request
        response = RequestResponse(request)
        # if response.status_code == 200:  # 检查接口返回码
        #     log.error(f"接口返回码是 【 {response.status_code} 】, 返回信息：{response.data_dict}")
        return response
    except Exception as e:  # 捕获异常
        log.error(f"请求学校课程时发生异常: {str(e)}")
        return None


if __name__ == '__main__':
    result = get_school_courses()  # 避免覆盖函数名
    print(result)
