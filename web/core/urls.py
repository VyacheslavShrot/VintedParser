from fastapi import FastAPI

from web.core.apis.webhook import WebHookHandler


def register_routes(app: FastAPI) -> None:
    webhook_handler: WebHookHandler = WebHookHandler()

    app.post("/tg-webhook")(webhook_handler.webhook)
