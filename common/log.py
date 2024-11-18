import logging  # 导入 Python 内置的日志模块
import sys  # 导入与系统交互的模块
from functools import wraps  # 导入 wraps 函数，用于保留被装饰函数的元数据
from common.tools import find_all_results


# TODO: 使用aspectlib，Aspect-Oriented Programming (AOP)，来改造。

# 定义一个函数，用于重置并重新配置日志记录器的处理程序
def _reset_logger(log):
    # 关闭并移除日志记录器的所有现有处理程序
    for handler in log.handlers:
        handler.close()  # 关闭当前处理程序，释放资源
        log.removeHandler(handler)  # 从日志记录器中移除处理程序
        del handler  # 删除处理程序对象以释放内存

    # 确保日志记录器的处理程序列表为空，并防止日志记录器向上级传播日志消息
    log.handlers.clear()
    log.propagate = False

    # 创建一个处理程序，用于将日志输出到控制台（标准输出）
    console_handle = logging.StreamHandler(sys.stdout)
    # 设置控制台输出的日志格式
    console_handle.setFormatter(
        logging.Formatter(
            "[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",  # 设置时间戳格式
        )
    )

    # 创建一个处理程序，用于将日志记录到文件 'run.log'，使用 UTF-8 编码
    file_handle = logging.FileHandler("run.log", encoding="utf-8")
    # 设置文件输出的日志格式，与控制台输出格式一致
    file_handle.setFormatter(
        logging.Formatter(
            "[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    # 将两个处理程序（控制台和文件）添加到日志记录器
    log.addHandler(file_handle)  # 将日志输出到文件
    log.addHandler(console_handle)  # 将日志输出到控制台


# 定义一个函数，用于获取并配置日志记录器
def _get_logger():
    # 获取一个名为 "log" 的日志记录器实例
    log = logging.getLogger("log")
    # 重置并重新配置日志记录器
    _reset_logger(log)
    # 设置日志记录器的日志级别为 INFO，处理 INFO 及以上级别的日志
    log.setLevel(logging.INFO)
    return log  # 返回配置好的日志记录器实例


# TODO: _log_code_decorator和_log_decorator重复的内容太多了，要优化。
def _log_decorator(*args, **kwargs):
    """
    日志装饰器，用于记录函数的开始、成功和失败信息。

    :param name_log_var: 自定义记录开始信息的变量名
    :param success_log_var: 自定义记录成功信息的变量名，默认为返回值
    :param error_log_var: 自定义记录错误信息的变量名，默认为异常信息
    """
    name_log_var = kwargs.get('name_log_var', None)
    success_log_var = kwargs.get('success_log_var', None)
    error_log_var = kwargs.get('error_log_var', None)

    def decorator(func):
        @wraps(func)  # 保留被装饰函数的元数据
        def wrapper(*args, **kwargs):
            class_name = args[0].__class__.__name__ if args else None  # 获取调用方法所在的类名
            method_name = func.__name__  # 获取方法名
            where_log = f"{class_name}.{method_name}"
            # 构建日志信息
            start_message = f"{class_name}.{method_name} - Start：{' ' + str(name_log_var) if name_log_var else ''}"
            _get_logger().info(start_message)  # 记录方法开始的日志

            try:
                result = func(*args, **kwargs)  # 执行被装饰的函数

                # 构建成功日志信息
                if success_log_var:
                    success_value = f"{locals().get('success_log_var')} - {str(result) if result is not None else 'result is None'}"
                elif name_log_var:
                    success_value = f"{name_log_var} - {str(result) if result is not None else 'result is None'}"
                else:
                    success_value = str(result) if result is not None else ''

                success_message = f"{class_name}.{method_name} - Success: {success_value}"
                _get_logger().info(success_message)  # 记录成功日志

                return result

            except Exception as e:
                # 构建错误日志信息
                if error_log_var is None:
                    error_value = str(e)
                elif name_log_var:
                    error_value = f"{name_log_var}{' - ' + str(e) if str(e) is not None else ''}"
                else:
                    error_value = f"{locals().get('error_log_var')}{' - ' + str(e) if str(e) is not None else ''}"
                error_message = f"{class_name}.{method_name} - Failed: {error_value}"
                _get_logger().error(error_message)  # 记录错误日志
                return None

        return wrapper  # 返回包装后的函数

    return decorator  # 返回装饰器函数


def _log_code_decorator(*args, **kwargs):
    """
    用于判定返回code是否复合预期，不能用于返回没有result中
    可以接受被修饰函数返回结果类型为dict
    :param args:
    :param kwargs:
    :return:
    """
    expected_key = kwargs.get('expected_key', "code")  # 默认期望判断的键为"code"
    expected_value = kwargs.get('expected_value', 200)  # 默认期望判断的值为200
    name_log_var = kwargs.get('name_log_var', None)
    success_log_var = kwargs.get('success_log_var', None)
    error_log_var = kwargs.get('error_log_var', None)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            class_name = args[0].__class__.__name__ if args else None  # 获取调用方法所在的类名
            method_name = func.__name__  # 获取方法名
            where_log = f"{class_name}.{method_name}"
            # 构建日志信息
            start_message = f"{class_name}.{method_name} - Start：{' ' + str(name_log_var) if name_log_var else ''}"
            _get_logger().info(start_message)  # 记录方法开始的日志

            # 兼容数据格式dict\tuple\list
            try:
                result = func(*args, **kwargs)  # 执行被装饰的函数
                # 判断返回值的类型并获取预期值,dict\tuple\list
                if isinstance(result, (dict, tuple, list)):
                    actual_value_list = find_all_results(result, expected_key)
                else:
                    actual_value_list = []

                if actual_value_list:
                    actual_value = actual_value_list[0]
                else:
                    actual_value = None

                # 检查返回值中的 code 字段
                if actual_value == expected_value:

                    # 构建成功日志信息
                    if success_log_var:
                        success_value = f"{locals().get('success_log_var')} - {str(result) if result is not None else 'result is None'}"
                    elif name_log_var:
                        success_value = f"{name_log_var} - {str(result) if result is not None else 'result is None'}"
                    else:
                        success_value = str(result) if result is not None else ''

                    success_message = f"{class_name}.{method_name} - Success: {success_value}"
                    _get_logger().info(success_message)  # 记录成功日志

                else:
                    # 构建错误日志信息
                    if error_log_var is None:
                        error_value = f"{str(result) if result else ''}"
                    if name_log_var:
                        error_value = f"{name_log_var} - {str(result) if result is not None else 'result is None'}"
                    else:
                        error_value = f"{locals().get('error_log_var')} - {str(result) if result is not None else 'result is None'}"
                    error_message = f"{class_name}.{method_name} - Failed: {error_value}"
                    _get_logger().error(error_message)  # 记录错误日志

                return result

            except Exception as e:
                # 处理函数执行期间的异常并记录错误日志
                if error_log_var is None:
                    error_value = str(e)
                if name_log_var:
                    error_value = f"{name_log_var}{' - ' + str(e) if str(e) is not None else ''}"
                else:
                    error_value = f"{locals().get('error_log_var')}{' - ' + str(e) if str(e) is not None else ''}"
                error_message = f"{class_name}.{method_name} - Failed: {error_value}"
                _get_logger().error(error_message)
                raise e  # 重新引发异常，或者根据需要处理

        return wrapper

    return decorator


class LogMeta(type):
    def __new__(cls, name, bases, dct):
        for attr_name, attr_value in dct.items():
            if callable(attr_value) and not attr_name.startswith('__'):
                # 检查方法是否标记为跳过日志
                if getattr(attr_value, '_skip_log', False):
                    continue
                # 获取自定义日志参数
                log_args = getattr(attr_value, '_log_args', {})
                dct[attr_name] = _log_decorator(**log_args)(attr_value)
        return super().__new__(cls, name, bases, dct)


# TODO: 有点凌乱，需要优化代码。增加可编辑性能和可读性。
def skip_log(func):
    """装饰器：标记跳过日志"""
    func._skip_log = True
    return func


def log_with(**log_args):
    """装饰器：为方法指定特定的日志参数"""
    name_log_var = log_args.get('name_log_var', None)
    success_log_var = log_args.get('success_log_var', None)
    error_log_var = log_args.get('error_log_var', None)

    def decorator(func):
        func._log_args = log_args
        return func

    return decorator


# 创建并配置全局日志记录器实例，可以在整个应用程序中使用,是个装饰器
log_dec = _log_decorator
# 创建并配置全局日志记录器实例，可以在整个应用程序中使用,是个装饰器
log_code_dec = _log_code_decorator
# 创建并配置全局日志记录器实例，可以在整个应用程序中使用，函数供单独使用
log = _get_logger()

if __name__ == "__main__":
    log.info(f"{sys.argv[0]}-This is an info message.")
    log.error("This is an error message.")
