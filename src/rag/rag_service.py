from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

class RagSummarizeService:
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model  
        self.chain = self._init_chain()

    def _init_chain(self):
        return self.prompt_template | print_prompt |self.model | StrOutputParser()

    def rag_summarize(self,query: str):
        docs =self.retriever.invoke(query)
        documents = ""
        counter = 0
        for doc in docs:
            counter += 1
            documents += f"【参考资料{counter}】：{doc.page_content}| 元数据：{doc.metadata}\n"
        return self.chain.invoke({"input": query, "context": documents})



if __name__ == '__main__':
    rag = RagSummarizeService()

    print(rag.rag_summarize("小户型适合哪些扫地机器人"))
