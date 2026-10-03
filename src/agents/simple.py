from typing import TypedDict
from langgraph.graph.message import MessagesState
from langchain_core.messages import AIMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
import random

VectorStorage = "vs_6abf2df0b2bc8191b8f9871cd0523e33"
# LLM instanciacion
# llm = init_chat_model(
#     model="gpt-4o",
#     temperature=1
# )

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=1
)

# memoria de estado de los mensajes, es decir el aray donde se guarda la conversación
class State(MessagesState):
    user_name: str
    my_age: int


state: State = {}
user_name = state.get("user_name", None)
print(user_name)

def node_1(state: State):
    
    new_state: State = {}
    
    if state.get("user_name") is None:
        new_state["user_name"] = "Juan Doe"
    else:
        new_state["my_age"] = random.randint(20,30)
    history = state["messages"]
    # le envio todo el historial de mensaje al llm
    ai_msg = llm.invoke(history)
    print(ai_msg)
    # y la respuesta de la ia se agrega a new state
    new_state["messages"] = [ai_msg]
    print(new_state)
    return new_state


builder = StateGraph(State)
builder.add_node("node_1", node_1)

# connections
builder.add_edge(START, 'node_1')
builder.add_edge('node_1', END)

# compile the entire angent

agent = builder.compile()