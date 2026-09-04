from dotenv import load_dotenv
from anthropic import Anthropic
import os

load_dotenv()
client = Anthropic()

tools = [
    {
        "name": "read_file",
        "description": "Reads the contents of a file at a given relative path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The relative path to the file to read."
                }
            },
            "required": ["path"]
        },

    },
    {
        "name": "list_files",
        "description": "Lists the files in a given directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The relative path to the directory to list."
                }
            },
            "required": ["directory"]
        },

    }
]

conversations = [
    {"role": "user", "content": "What files are in this directory? Then read the most interesting one and summarise it."}
]
def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

def list_files(directory: str) -> list:
    return "\n".join(os.listdir(directory))
REGISTRY = {
    "read_file": read_file,
    "list_files": list_files
}
while True:
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        tools=tools,
        messages=conversations
)
    if response.stop_reason != "tool_use":
        break
    results = []
    conversations.append({"role": "assistant", "content": response.content})
    for block in response.content:
        if block.type == "tool_use":
            fn = REGISTRY[block.name]
            ans = fn(**block.input)
            
            results.append({"type": "tool_result", "tool_use_id": block.id, "content": ans})
    conversations.append({"role": "user", "content": results})

print(response)
