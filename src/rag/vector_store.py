from codecs import lookup

from langchain_chroma import Chroma
from langchain_core.documents import Document
from model.factory import embed_model
from utils.config_handler import chroma_conf

from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tool import get_abs_path
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger
import os


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=get_abs_path(chroma_conf["persist_directory"]),
        )

        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len
        )
    
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})
    
    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        要计算文件的MD5做去重
        :return: None
        """
        #返回false表示没有处理过，返回true表示处理过了
        def check_md5_hex(md5_hex):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]), 'w',encoding='utf-8').close()
                return False
            with open(get_abs_path(chroma_conf["md5_hex_store"]), 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() == md5_hex:
                        return True
            return False

        def save_md5_hex(md5_hex):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), 'a', encoding='utf-8') as f:
                f.write(md5_hex + '\n')
        
        #识别文件后缀，读取内容
        def get_file_documents(read_path: str):
            if read_path.endswith('.pdf'):
                return pdf_loader(read_path)
            elif read_path.endswith('.txt'):
                return txt_loader(read_path)
            return []
        
        #获取可读文件列表
        allowed_files_path:list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]), 
            tuple(chroma_conf["allow_knowledge_file_type"]),
        )

        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue
            
            try:
                documents:list[Document] = get_file_documents(path)
                if not documents:
                    logger.warning(f"[加载知识库]文件 {path} 读取失败或没有内容，跳过")
                    continue
                
                #文本切分
                split_docs:list[Document] = self.spliter.split_documents(documents)
                #向量化并存储
                self.vector_store.add_documents(split_docs)
                #记录MD5
                save_md5_hex(md5_hex)
                logger.info(f"[加载知识库]文件 {path} 处理完成，已存入知识库")
            except Exception as e:
                logger.error(f"[加载知识库]处理文件 {path} 时发生错误: {str(e)}")
                continue

if __name__ == '__main__':
    vs = VectorStoreService()

    vs.load_document()

    retriever = vs.get_retriever()

    res = retriever.invoke("迷路")
    for r in res:
        print("-"*20)
        print(r.page_content)
        print("-"*20)
