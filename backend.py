from graph_builder import workflow
from dotenv import load_dotenv
load_dotenv()

def generate_blog(title: str):
    result = workflow.invoke({"title": title})

    print(result)

    return result["content"].content[0]["text"]