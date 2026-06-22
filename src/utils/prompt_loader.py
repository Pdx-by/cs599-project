from utils.config_handler import prompts_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger


def load_system_prompts():
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except Exception as e:
        logger.error(f"[load_system_prompt]获取系统提示词路径失败，错误信息：{str(e)}")
        raise e
    try:
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        return system_prompt
    except Exception as e:
        logger.error(f"[load_system_prompt]加载系统提示词失败，错误信息：{str(e)}")
        raise e
    
def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except Exception as e:
        logger.error(f"[load_rag_prompt]获取RAG提示词路径失败，错误信息：{str(e)}")
        raise e
    try:
        with open(rag_prompt_path, 'r', encoding='utf-8') as f:
            rag_prompt = f.read()
        return rag_prompt
    except Exception as e:
        logger.error(f"[load_rag_prompt]加载RAG提示词失败，错误信息：{str(e)}")
        raise e

def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except Exception as e:
        logger.error(f"[load_report_prompt]获取报告提示词路径失败，错误信息：{str(e)}")
        raise e
    try:
        with open(report_prompt_path, 'r', encoding='utf-8') as f:
            report_prompt = f.read()
        return report_prompt
    except Exception as e:
        logger.error(f"[load_report_prompt]加载报告提示词失败，错误信息：{str(e)}")
        raise e

if __name__ == "__main__":
    print(load_system_prompts())
    # print(load_rag_prompt())
    # print(load_report_prompt())