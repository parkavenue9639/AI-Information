from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os
import pymysql
from pydantic import BaseModel, Field

os.environ["DEEPSEEK_API_KEY"] = "sk-003194da3682421199b4954861ad3082"

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'ai_news',
    'charset': 'utf8mb4'
}

class Summary(BaseModel):
    summary: str = Field(description="ai摘要")
    region: str = Field(description="国内 | 国外")

def get_and_summarize_data_from_db():
    # 获取db中详细数据
    conn = pymysql.connect(**db_config)
    read_cursor = conn.cursor()
    write_cursor = conn.cursor()
    try:
        # 1.读取所有记录的id和detail
        read_cursor.execute('select id, detail, title from news_flash')
        for row in read_cursor:
            news_id, detail, title = row
            print("正在摘要 ID={} title={}".format(news_id, title))
            # print("总结前： {}".format(detail))
            summary_result = generate_summary(detail)
            if summary_result:
                # 重新写回db
                print("DeepSeek总结： {}".format(summary_result["summary"]))
                print("地区分类： {}".format(summary_result["region"]))
                write_cursor.execute(
                    "UPDATE news_flash SET summary=%s, region=%s WHERE id=%s",
                    (summary_result["summary"], summary_result["region"], news_id)
                )
                print("摘要已更新")
        conn.commit()
    except Exception as e:
        print("数据库处理失败： {}".format(e))
    finally:
        read_cursor.close()
        write_cursor.close()
        conn.close()

def generate_summary(detail):
    # 调用api进行总结改写

    # 创建Pydantic解析器
    parser = JsonOutputParser(pydantic_object=Summary)
    # 获取格式说明
    format_instructions = parser.get_format_instructions()
    # 创建包含格式指令的提示模板
    prompt_template = ChatPromptTemplate(
        [("system", "你是一个AI行业专家，总结以下AI行业新闻核心内容，尽量多的包含信息，超过45个字符，但是不能输出超过60个字符，且区分是国内还是国外的信息。\n\n{format_instructions}"),
        MessagesPlaceholder("msg"),],
        partial_variables={"format_instructions": format_instructions}

    )
    # prompt = prompt_template.invoke({"msg": [("user", detail)]})

    query_dict = {
        "msg": [("user", detail)],
    }

    # 简易写法
    '''messages = [
        (
            "system",
            "你是一个AI行业专家，总结以下AI行业新闻核心内容，尽量多的包含信息，但是不能输出超过60个字符：",
        ),
        ("human", detail),
    ]
    ai_msg = llm.invoke(messages)
    '''
    # 构建完整的处理链
    chain = prompt_template | llm | parser
    # 执行链并返回结构化数据
    ai_msg = chain.invoke(query_dict)
    return ai_msg

if __name__ == '__main__':
    get_and_summarize_data_from_db()