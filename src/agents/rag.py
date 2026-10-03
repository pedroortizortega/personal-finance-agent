from typing import TypedDict
from langgraph.graph.message import MessagesState
from langchain_core.messages import AIMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
import random
from pydantic import BaseModel, Field
import os


class ContactInfo(BaseModel):
    name: str = Field(..., description="The name of the person")
    email: str = Field(..., description="The email address of the person")
    phone: str = Field(..., description="The phone number of the person")
    age: int = Field(..., description="The age of the person")

    

##### config Agent

# Id del vector storage que esta en OpenIA
VectorStorage = [os.getenv("VECTOR_STORE_ID")]

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=1
)

# declaracion para el usar el file search tool de OpenAI
file_search_tool = {
    "type": "file_search",
    "vector_store_ids": VectorStorage
}


llm_with_structured_output = ChatOpenAI(
    model="gpt-4o",
    temperature=1
    )


llm = llm.bind_tools([file_search_tool])

llm_with_structured_output = llm_with_structured_output.with_structured_output(
    ContactInfo
    )

#####


# memoria de estado de los mensajes, es decir el aray donde se guarda la 
# conversación
class State(MessagesState):
    user_name: str
    phone: str
    my_age: int


def extractor(state: State):
    history = state["messages"]
    user_name = state.get("user_name", None)
    new_state: State = {}
    # la invocación del llm con salida estructurada se hace solo si no tenemos 
    # el nombre del usuario o si el historial de mensajes es mayor a 10, esto 
    # para evitar que el modelo haga la extracción de información en cada 
    # mensaje y solo lo haga cuando sea necesario.
    if user_name is None or len(history) > 10:
        # Utilizo el llm con salida estructurada para extraer la información 
        # del usuario
        schema = llm_with_structured_output.invoke(history)
        # De la respuesta que es la salida la agrego al nuevo estado
        new_state["user_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age
    return new_state


def conversation(state: State):
    new_state: State = {}
    history = state["messages"]
    last_msg = history[-1]
    user_name = state.get("user_name", "Juan Doe")
    system_msg = f"""You are a helpful assistant that can answer questions about  
    the user {user_name}."""
    # le envio todo el historial de mensaje al llm
    ai_msg = llm.invoke([("system", system_msg), ("user", last_msg.text)])
    new_state["messages"] = [ai_msg]
    return new_state


builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)

# connections
builder.add_edge(START, 'extractor')
builder.add_edge('extractor', 'conversation')
builder.add_edge('conversation', END)

# compile the entire angent

agent = builder.compile()