from fastapi import FastAPI, HTTPException, Request
from starlette.responses import JSONResponse

from bot.config.settings import on_startup, on_shutdown
from web.core.urls import register_routes

# Create Web APP FastAPI
app: FastAPI = FastAPI(
    title="Vinted Parser Bot"
)


class AppDefaultHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        SingleTone Pattern
        """
        if not cls._instance:
            return super(AppDefaultHandler, cls).__new__(cls)
        if cls._instance:
            raise Exception("Only one instance of AppHandler can be created.")

    @staticmethod
    async def custom_http_exception_handler(
            request: Request,
            exc: HTTPException
    ) -> JSONResponse:
        """
        Custom HTTPException Response
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail
            }
        )

    @staticmethod
    async def startup():
        """
        Connect To DataBase and Bot WebHook
        """
        await on_startup(app)

    @staticmethod
    async def shutdown():
        """
        Disconnect To DataBase and Bot WebHook
        """
        await on_shutdown(app)


app_default_handler: AppDefaultHandler = AppDefaultHandler()

app.add_exception_handler(HTTPException, app_default_handler.custom_http_exception_handler)

app.add_event_handler("startup", app_default_handler.startup)
app.add_event_handler("shutdown", app_default_handler.shutdown)

# Register Another Routes
register_routes(app)
