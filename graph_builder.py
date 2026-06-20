# %%
from langgraph.graph import StateGraph,START,END
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()



# %%
model=ChatHuggingFace(
    llm=HuggingFaceEndpoint(
        model="deepseek-ai/DeepSeek-V3.2",
        # model="Qwen/Qwen3-32B",
        temperature=0.7
    )
)


# model = ChatGoogleGenerativeAI(
#     model="gemini-flash-latest", # Changed model name to gemini-flash-latest based on available models
#     temperature=0,
#     # timeout=15
# )

# %%
class BLOGState(TypedDict):
    title:str
    outline:str
    content:str

# %%
def create_outline(state:BLOGState)->BLOGState:
    title=state['title']

    prompt=f"GENERATE AN OUTLINE FOR A BLOG ON THE TOPIC : {title}"

    outline=model.invoke(prompt).content

    state['outline']=outline

    return state
    

# %%
def create_blog(state:BLOGState)->BLOGState:
    outline=state['outline']
    title=state['title']

    prompt=f"Write a detailed blog on the title {title}using the following outline \n{outline}. use the proper indentation and spacing and keep the tone light and funny. make the response very creative,phylosphical,logical and witty also use the emojies in abundence to make it viusllly amazing , also you can use any prose or quote stated by any person or prose of peom or any shayri or amaing thouths"

    state['content']=model.invoke(prompt)

    return state



    


# %%
graph=StateGraph(BLOGState)

graph.add_node('create_outline',create_outline)
graph.add_node('create_blog',create_blog)

graph.add_edge(START,'create_outline')
graph.add_edge('create_outline','create_blog')
graph.add_edge('create_blog',END)

workflow=graph.compile()

# %%
# inputs={
#     'title':"people save reels and posts on insta but never get time to watch them later",
# }

# blog=workflow.invoke(inputs)
# # print(workflow.invoke(inputs)['outline'])
# print(blog['content'].content)


# %%
import sys
print(sys.executable)


