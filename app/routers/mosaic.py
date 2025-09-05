from fastapi import APIRouter, HTTPException
from titiler.mosaic.factory import MosaicTilerFactory

from .. import backend, utils
from ..config import get_config

# Mosaic tiler
mosaic_tiler = MosaicTilerFactory(router_prefix="/mosaic", path_dependency=backend.get_mosaic_path)
router = APIRouter()
router.include_router(mosaic_tiler.router)


config = get_config()


@router.post("/create-mosaic")
async def create_mosaic():
    name = config.name
    raster_dir = config.raster_dir
    cache_dir = config.cache_dir

    cog_files = utils.get_cog_files(raster_dir)
    if not cog_files:
        raise HTTPException(status_code=404, detail="No COG files found!")

    mosaic_path = f"{cache_dir}/{name}_mosaic.json"
    utils.create_mosaic_json(cog_files, mosaic_path)

    return {"status": "success", "files": len(cog_files), "mosaic_path": str(mosaic_path)}
