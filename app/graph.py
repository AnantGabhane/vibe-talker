from typing import Annotated
from typing_extensions import TypedDict
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY environment variable is not set. Please set it in your .env file."
    )
os.environ["GOOGLE_API_KEY"] = api_key


class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def run_command(cmd: str):
    """Take a command line promt and execute it on the user's machine and returns the output of the command.
    Example: run_command(cmd="ls") where ls is the command to list the files
    """
    result = os.system(command=cmd)
    return result


llm = init_chat_model("google_genai:gemini-2.0-flash")
llm_with_tools = llm.bind(tools=[run_command])


def chatbot(state: State):
    system_prompt = SystemMessage(
        content="""
    You are an advanced AI coding assistant that executes commands, generates code, and manages files intelligently.

    Your responsibilities:

    1. **Command and Tool Execution**
       - Analyze the user’s intent and select the correct tool or command to achieve it.
       - Execute commands safely and display results clearly.

    2. **File Management**
       - Always save generated code or output files inside a directory named `ai_generated` located in the **current working directory** (not the system root).
         Example path: `./ai_generated/`
       - Before saving, ensure the folder exists:
         - Check if `./ai_generated` exists.
         - If not, create it using a command such as:
           ```bash
           mkdir -p ./ai_generated
           ```
       - Handle permission errors gracefully and suggest correct paths if needed.
       - Confirm successful file creation or update after saving.

    3. **Best Practices**
       - Never attempt to create directories directly under `/` (system root) unless explicitly requested by the user.
       - Keep responses concise, structured, and focused on execution outcomes.
       - Clearly show command outputs or error messages.
       - Prioritize reliability and safety in all operations.

    **Your Goal:** Act as a dependable AI developer assistant who can write, execute, and save working code with full autonomy, ensuring all generated files are properly organized under `./ai_generated/`.
    """
    )

    message = llm_with_tools.invoke([system_prompt] + state["messages"])
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}


tool_node = ToolNode(tools=[run_command])
# build graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()


# creates a new graph with given checkpointer
def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)
