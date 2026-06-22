import os
import hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


#获取文件的md5值，返回16进制字符串表示的md5值
def get_file_md5_hex(filepath:str)->str:
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]文件{filepath}不存在")
        return None
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]文件{filepath}不是文件")
        return None
    md5 = hashlib.md5()

    chunk_size = 4096  # 4KB分片加载到内存避免文件过大出错
    try:
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                md5.update(chunk)       #每4kb更新一次md5计算，直到文件读完
        return md5.hexdigest()          #得到最终的md5值，返回16进制字符串表示的md5值
    except Exception as e:
        logger.error(f"[md5计算]计算文件{filepath}的md5失败，错误信息：{str(e)}")
        return None

#批量处理path文件夹下，list[]包含类型的文件
def listdir_with_allowed_type(path:str, allowed_types:tuple[str])->tuple[str]:
    files = []
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]路径{path}不存在或不是文件夹")
        return allowed_types
    for f in os.listdir(path):
        if f.endswith(allowed_types):   #检查文件是否以allowed_types中的任一类型结尾，符合条件则添加到列表中
            files.append(os.path.join(path, f)) #将符合条件的文件路径添加到列表中，使用os.path.join确保路径正确
    
    return tuple(files)     #返回一个包含所有符合条件的文件路径的元组，元组不可修改，保证数据安全性

def pdf_loader(filepath:str,password=None)->list[Document]:
    return PyPDFLoader(filepath,password).load()

def txt_loader(filepath:str)->list[Document]:
    return TextLoader(filepath,encoding='utf-8').load()