from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .settings import get_config
from .routes import register_routes

def create_app(config="dev"):
    settings = get_config(config=config)

    app = FastAPI(title="Data Analyze")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_routes(app)

    @app.get("/")
    def index():
        return settings.CONFIG_NAME

    @app.get("/health")
    def health():
        return {"status": "healthy"}

    return app
