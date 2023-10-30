import json
import os
import openai
from quart import Quart
from quart import Blueprint, Response, current_app, render_template, request, stream_with_context

bp = Blueprint("app", __name__, template_folder="templates", static_folder="static")

@bp.before_app_serving
async def configure_openai():
    openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_version = "2023-07-01-preview"
    openai.api_type = "azure"
    openai.api_key = os.getenv("AZURE_OPENAI_KEY")

@bp.get("/")
async def index():
    return await render_template("index.html")

@bp.post("/chat")
async def chat_handler():
    request_message = (await request.get_json())["message"]

    @stream_with_context
    async def response_stream():
        chat_coroutine = openai.ChatCompletion.acreate(
            engine = "gpt-35-turbo", # The deployment name you chose when you deployed the GPT-35-turbo or GPT-4 model.
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request_message},
            ],
            temperature = 0.7,
            max_tokens = 1024,
            top_p = 0.95,
            frequency_penalty = 0,
            presence_penalty = 0,
            stop = None,
            stream = True,
        )
        async for event in await chat_coroutine:
            # "2023-07-01-preview" API version has a bug where first response has empty choices
            if event["choices"]:
                current_app.logger.info(event)
                yield json.dumps(event, ensure_ascii=False) + "\n"

    return Response(response_stream())

if __name__ == "__main__":
    app = Quart(__name__)
    app.register_blueprint(bp)
    app.run()