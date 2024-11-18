import json
# import ymal
import sys
import time
from configparser import ConfigParser
from datetime import datetime, timedelta


class MyConfigParser(ConfigParser):
    """
    重写 configparser 中的 optionxform 函数，解决 .ini 文件中的 键option 自动转为小写的问题
    """

    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class ReadFileData:

    def __init__(self):
        pass

    # def load_yaml(self, file_path):
    #     """
    #     加载yaml，暂时不用
    #     :param file_path:
    #     :return:
    #     """
    #     log.info("加载 {} 文件......".format(file_path))
    #     with open(file_path, encoding='utf-8') as f:
    #         data = yaml.safe_load(f)
    #     log.info("读到数据 ==>>  {} ".format(data))
    #     return data

    def load_json(self, file_path):
        from common.log import log
        try:
            log.info("加载 {} 文件......".format(file_path))
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            log.info("读到数据 ==>>  {} ".format(data))
            return data
        except FileNotFoundError as e:
            log.error(f"{sys.argv[0]}-配置文件未找到: {e}")
            raise
        except json.JSONDecodeError as e:
            log.error(f"{sys.argv[0]}-配置文件解析失败: {e}")
            raise
        except KeyError as e:
            log.error(f"{sys.argv[0]}-配置文件中未找到字段 '{e}'")
            raise

    def load_ini(self, file_path):
        from common.log import log
        try:
            log.info("加载 {} 文件......".format(file_path))
            config = MyConfigParser()
            config.read(file_path, encoding="UTF-8")
            data = dict(config._sections)
            log.info("读到数据 ==>>  {} ".format(data))
            return data
        except FileNotFoundError as e:
            log.error(f"{sys.argv[0]}-配置文件未找到: {e}")
            raise


def get_timestamp():
    """
    获取当前时间戳
    :return: 时间戳字符串
    """
    return str(int(time.time() * 1000))


def get_current_date(**kwargs):
    """
    获取当前日期
    :return: 当前日期格式，默认格式为%Y-%m-%d
    """
    format_data = kwargs.get('format', '%Y-%m-%d')
    # 获取当前日期
    current_date = datetime.now()
    formatted_date = current_date.strftime(format_data)

    return formatted_date


def calculate_date(**kwargs):
    """
        计算从当前日期起，向前或向后推移指定天数后的日期，并根据格式进行格式化。
    :param kwargs: days向前或向后推移的天数（负数表示向前，正数表示向后） format_data日期格式，默认为 'YYYY-MM-DD'
    :return:  格式化后的日期字符串
    """
    days = kwargs.get('days', 0)
    format_data = kwargs.get('format', '%Y-%m-%d')
    start_data = kwargs.get('start_data', datetime.now())
    target_date = start_data + timedelta(days=days)
    formatted_date = target_date.strftime(format_data)

    return formatted_date


def find_all_results(data, key):
    """
    递归函数来遍历字典中的所有键
    :param data: 被查找对象
    :param key: 键
    :return:输出值列表
    """
    results = []

    # 如果当前对象是字典
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                results.append(v)  # 如果找到目标键，则将值添加到列表中
            else:
                results.extend(find_all_results(v, key))  # 递归搜索嵌套字典或列表

    # 如果当前对象是列表
    elif isinstance(data, (list, tuple)):
        for item in data:
            results.extend(find_all_results(item, key))  # 递归搜索嵌套字典或列表

    return results
