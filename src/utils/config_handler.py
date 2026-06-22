"""
yaml配置文件相当于字典
"""

import yaml
from utils.path_tool import get_abs_path

def load_rag_config(config_file: str = get_abs_path("config/rag.yml"),encoding: str = 'utf-8') -> dict:
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)   #全部加载
    return config

def load_prompt_config(config_file: str = get_abs_path("config/prompt.yml"),encoding: str = 'utf-8') -> dict:
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)   #全部加载
    return config

def load_chroma_config(config_file: str = get_abs_path("config/chroma.yml"),encoding: str = 'utf-8') -> dict:
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)   #全部加载
    return config

def load_agent_config(config_file: str = get_abs_path("config/agent.yml"),encoding: str = 'utf-8') -> dict:
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)   #全部加载
    return config

#快捷获取
rag_conf = load_rag_config()
prompts_conf = load_prompt_config()
chroma_conf = load_chroma_config()
agent_conf = load_agent_config()

if __name__ == "__main__":
    print(rag_conf["chat_model_name"])
