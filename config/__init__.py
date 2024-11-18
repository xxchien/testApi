import os
from common import load_data

# 项目根目录路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# 配置文件路径
SETTING_FILE_PATH = os.path.join(BASE_PATH, "config", "setting.ini")

# 加载配置文件，获取 API 主机地址
api_host = load_data.load_ini(SETTING_FILE_PATH)["host"]["api_host"]

# 测试用例集路径
CASE_DIR = os.path.join(BASE_PATH, "case")

# 测试用例结果目录
PRPORE_JSON_DIR = os.path.join(BASE_PATH, "output", "report_json")

# 测试结果报告目录
PRPORE_ALLURE_DIR = os.path.join(BASE_PATH, "output", "report_allure")

if __name__ == "__main__":
    print(f"Base Path: {BASE_PATH}")
    print(f"Setting File Path: {SETTING_FILE_PATH}")
    print(f"Case Directory: {CASE_DIR}")
    print(f"Report JSON Directory: {PRPORE_JSON_DIR}")
    print(f"Report Allure Directory: {PRPORE_ALLURE_DIR}")
    print(f"API Host: {api_host}")