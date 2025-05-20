import base64
from agent.agent import Agent
from computers.default import LocalPlaywrightBrowser

tools = [
    {
        "type": "function",
        "name": "back",
        "description": "Go back to the previous page.",
        "parameters": {},
    },
    {
        "type": "function",
        "name": "goto",
        "description": "Go to a specific URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Fully qualified URL to navigate to.",
                },
            },
            "additionalProperties": False,
            "required": ["url"],
        },
    },
    {
        "type": "function",
        "name": "upload_file",
        "description": "Upload a file to the current page.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "integer",
                    "description": "The x coordinate of the file input.",
                },
                "y": {
                    "type": "integer",
                    "description": "The y coordinate of the file input.",
                },
                "file_payloads": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the file",
                            },
                            "mimeType": {
                                "type": "string",
                                "description": "The MIME type of the file",
                            },
                            "buffer": {
                                "type": "string",
                                "format": "byte",
                                "description": "The file content as base64 encoded bytes",
                            },
                        },
                        "required": ["name", "mimeType", "buffer"],
                    },
                    "description": "Array of FilePayload objects with name, mimeType, and buffer properties",
                },
            },
        },
    },
]


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def main():
    base64_image = encode_image("lowes-test-image.jpg")
    with LocalPlaywrightBrowser() as computer:
        agent = Agent(computer=computer, tools=tools)
        items = [
            {
                "role": "developer",
                "content": "Use the additional back() and goto() and upload_file() functions to navigate the browser and upload files.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Use this image when uploading a file.",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            },
        ]

        while True:
            user_input = input("> ")
            items.append({"role": "user", "content": user_input})
            output_items = agent.run_full_turn(items, show_images=False)
            items += output_items


if __name__ == "__main__":
    main()
