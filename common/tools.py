import json
import os
# import ymal
import sys
from configparser import ConfigParser


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
            # log.info("读到数据 ==>>  {} ".format(data))
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


class SaveFile:
    def __init__(self):
        pass

    def save_json_to_file(self, data_json, file_path: str):
        """
        将 JSON 数据保存到指定文件中。如果 data_json 已经是 JSON 字符串，则直接保存。
        :param data_json: 需要保存的 JSON 数据，支持字典、列表或已处理的 JSON 字符串
        :param file_path: 保存文件的完整路径
        """
        # 确保文件夹存在
        folder_path = os.path.dirname(file_path)
        os.makedirs(folder_path, exist_ok=True)

        # 判断 data_json 是否是字符串类型
        if isinstance(data_json, str):
            json_string = data_json  # 如果是字符串，直接使用
        else:
            import json
            json_string = json.dumps(data_json, ensure_ascii=False, indent=4)  # 如果是对象，先转换为字符串

        # 写入文件，覆盖已有内容
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(json_string)

    def save_to_file(self, data_json, file_path: str):
        """
        将 JSON 数据保存到指定文件中
        :param data_json: 需要保存的 JSON 数据
        :param file_path: 保存文件的完整路径
        """
        # 确保文件夹存在
        folder_path = os.path.dirname(file_path)
        os.makedirs(folder_path, exist_ok=True)

        # 写入文件，覆盖已有内容
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data_json, file, ensure_ascii=False, indent=4)
