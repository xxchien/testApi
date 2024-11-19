from json import JSONDecodeError
from core import RequestClient, RequestResponse
from config import *
from common import log, save_file, load_data


class SwaggerApi(RequestClient):
    """
    用于处理swagger上的接口文档，获取对应的接口
    """

    def __init__(self):
        super(SwaggerApi, self).__init__(api_host)
        self.session.headers = {
            "Host": self.api_host
        }

    def get_module_list(self):
        base_path = "/swagger-resources"
        request = self.get(base_path)
        module_list = RequestResponse(request).data_dict
        for item in module_list:
            if 'name' in item:
                item['name'] = item['name'].replace('-swagger', '')
        return module_list

    def get_module_docs(self, **kwargs):
        path = kwargs.get("module_path")
        request = self.get(path)
        try:
            module_docs = RequestResponse(request).data_dict
            return module_docs
        except JSONDecodeError:
            log.info("进入了错误")
            content = request.content.decode('utf-8')
            content = content.replace("false", "False").replace("true", "True").replace("null", "None")
            try:
                module_docs = eval(content)
                return module_docs
            except Exception as e:
                log.error(f"eval 执行失败: {e}")
                raise

    def save_module_docs(self, **kwargs):
        """
        获取 模块中的api 并保存到指定文件
        :param kwargs: 传递给 get_module_list 的其他参数
        """
        module_name = kwargs.get('module_name', None)
        module_path = kwargs.get('module_path', None)
        file_path = kwargs.get('file_path',
                               f"{os.path.join(API_DATA, f'{module_name}_api_docs.json')}")
        module_docs = self.get_module_docs(module_path=module_path)
        # 调用通用方法保存数据
        save_file.save_to_file(module_docs, file_path)

    def save_modules_docs(self):
        """
        获取 所有模块中的api 并保存到指定文件
        """
        module_list = load_data().load_json(
            f"{os.path.join(API_MODULE_LIST, 'module_list.json')}")
        for module in module_list:
            module_name = module['name']
            module_path = module['url']
            self.save_module_docs(module_name=module_name, module_path=module_path)

    def save_module_list(self, **kwargs):
        """
        获取 module_list_json 并保存到指定文件
        :param kwargs: 传递给 get_module_list 的其他参数
        """
        file_path = kwargs.get('file_path',
                               f"{os.path.join(API_MODULE_LIST, 'module_list.json')}")
        # 获取 module_list 数据
        module_list = self.get_module_list()
        # 调用通用方法保存数据
        save_file.save_to_file(module_list, file_path)


if __name__ == "__main__":
    # 用于更新 api——data
    swagger_api = SwaggerApi()
    # 更新module_list
    swagger_api.save_module_list()
    # 更新各模块的api_docs
    swagger_api.save_modules_docs()
