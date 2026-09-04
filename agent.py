from dotenv import load_dotenv
from anthropic import Anthropic

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

    }
]
conversations = [
    {"role": "user", "content": "What's in notes.txt?"}]
def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()
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
            ans = read_file(block.input["path"])
            
            results.append({"type": "tool_result", "tool_use_id": block.id, "content": ans})
    conversations.append({"role": "user", "content": results})

print(response)
