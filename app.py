import json
import os
from openai import AsyncAzureOpenAI,AzureOpenAI
from quart import Quart
from quart import Blueprint, Response, current_app, render_template, request, stream_with_context

bp = Blueprint("app", __name__, template_folder="templates", static_folder="static")

client = AsyncAzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

@bp.get("/")
async def index():
    return await render_template("index.html")

@bp.post("/chat")
async def chat_handler():
    request_message = (await request.get_json())["message"]

    @stream_with_context
    async def response_stream():
        chat_coroutine = client.chat.completions.create(
            model="gpt-35-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request_message},
            ],
            temperature = 0.0,
            max_tokens = 1024,
            stream=True,
        )

        async for event_chunk in await chat_coroutine:
            event = event_chunk.model_dump()  # Convert pydantic model to dict
            if event["choices"]:
                #print(event)
                yield json.dumps(event, ensure_ascii=False) + "\n"
                
    return Response(response_stream())

if __name__ == "__main__":
    app = Quart(__name__)
    app.register_blueprint(bp)
    app.run()