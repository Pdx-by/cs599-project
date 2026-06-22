"""
为整个工程提供统一绝对路径
"""
from multiprocessing import current_process
import os

def get_project_root() -> str:
    """
    获取项目根目录的绝对路径
    """
    #当前文件的绝对路径，即utils/path_tool.py的绝对路径
    current_process = os.path.abspath(__file__)
    #获取文件所在文件夹的绝对路径（即上层文件夹），即utils文件夹的绝对路径
    current_dir = os.path.dirname(current_process)
    #获取项目绝对路径，即上层文件夹的绝对路径，即项目根目录的绝对路径 /AgentProject
    project_root = os.path.dirname(current_dir)
    return project_root

def get_abs_path(relative_path: str) -> str:
    """
    将相对路径转换为绝对路径
    :param relative_path: 相对于项目根目录的路径
    :return: 绝对路径
    """
    project_root = get_project_root()
    abs_path = os.path.join(project_root, relative_path)
    return abs_path

if __name__ == "__main__":
    #测试函数
    print(get_project_root())
    print(get_abs_path("data/选购指南.txt"))
