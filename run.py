import pytest
from config import *
from common import *


class RunPytest:
    @staticmethod
    def run():
        """
        调试运行测试用例。
        :return: 无返回值
        """
        # 执行用例
        pytest.main(['--alluredir', f'{PRPORE_JSON_DIR}', f'{CASE_DIR}'])
        # 生成测试报告
        os.system(f'allure generate {PRPORE_JSON_DIR} -o {PRPORE_ALLURE_DIR} --clean')
        log.info('测试报告生成完成！')


if __name__ == '__main__':
    RunPytest.run()
