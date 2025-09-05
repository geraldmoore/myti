from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware

from . import utils
from .config import get_config
from .routers import aws, cog, mosaic, ui

config = get_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    name = config.name
    cache_dir = config.cache_dir
    mosaic_path = f"{cache_dir}/{name}_mosaic.json"

    if not Path(mosaic_path).exists():
        Path(cache_dir).mkdir(exist_ok=True)
        raster_dir = config.raster_dir
        cog_files = utils.get_cog_files(raster_dir)
        if cog_files:
            utils.create_mosaic_json(cog_files, mosaic_path)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Raster Tile Server", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(aws.router, prefix="/private/cog", tags=["Private COG"])
    app.include_router(cog.router, prefix="/cog", tags=["COG"])
    app.include_router(mosaic.router, prefix="/mosaic", tags=["Mosaic"])
    app.include_router(ui.router, tags=["UI"])

    return app


app = create_app()
