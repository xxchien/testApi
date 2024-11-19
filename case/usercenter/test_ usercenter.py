import pytest
import allure
from common import *
from operation.usercenter import get_school_courses


@allure.severity(allure.severity_level.TRIVIAL)
@allure.epic("针对单个接口的测试")
@allure.feature("获取用户信息模块")
class TestGetUserInfo:
    """获取用户信息模块"""

    @allure.story("用例--获取用户学校course信息")
    @allure.description("该用例是针对获取用户学校course信息")
    @allure.issue("https://e.gitee.com/unisolution_cn/projects/28863/milestones/206556/issues/table",
                  name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://e.gitee.com/unisolution_cn/projects/28863/milestones/206556/issues/table",
                     name="点击，跳转到对应用例的链接地址")
    def test_get_school_courses(self):
        log.info("*************** 开始执行用例 ***************")
        result = get_school_courses()
        assert result.status_code == 200
        log.info(f"code ==>> 期望结果：{200}， 实际结果：{result.status_code}")
        log.info("*************** 结束执行用例 ***************")
