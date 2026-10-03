# from langchain.tools import tool
# from langchain.chat_models import init_chat_model


# model = init_chat_model(
#     "claude-sonnet-4-6",
#     temperature=0
# )


# # Define tools
# @tool
# def multiply(a: int, b: int) -> int:
#     """Multiply `a` and `b`.

#     Args:
#         a: First int
#         b: Second int
#     """
#     return a * b


# @tool
# def add(a: int, b: int) -> int:
#     """Adds `a` and `b`.

#     Args:
#         a: First int
#         b: Second int
#     """
#     return a + b


# @tool
# def divide(a: int, b: int) -> float:
#     """Divide `a` and `b`.

#     Args:
#         a: First int
#         b: Second int
#     """
#     return a / b


# # Augment the LLM with tools
# tools = [add, multiply, divide]
# tools_by_name = {tool.name: tool for tool in tools}
# model_with_tools = model.bind_tools(tools)

from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get the current weather for a given city.

    Args:
        city: Name of the city to get the weather for.
    """
    return f"It's always sunny {city}"

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather],
    system_prompt="You are a helpful assitant"
)