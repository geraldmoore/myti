import json
from pathlib import Path
from typing import Any

from cogeo_mosaic.mosaic import MosaicJSON

from .auth import get_s3_client, init_aws_session


def list_objects(bucket: str, prefix: str, ext: str) -> list[str]:
    """List objects at bucket/prefix location."""
    session = init_aws_session()
    client = get_s3_client(session)
    paginator = client.get_paginator("list_objects_v2")
    files = []
    for subset in paginator.paginate(Bucket=bucket, Prefix=prefix):
        files.extend(subset.get("Contents", []))
    return [r["Key"] for r in files if r["Key"].endswith(ext)]


def get_cog_files_local(directory: str, ext: str) -> list[str]:
    """Get COG files from local directory."""
    return [str(f) for f in Path(directory).glob(f"*{ext}")]


def get_cog_files_s3(directory: str, ext: str) -> list[str]:
    """Get COG files from S3 directory."""
    path = directory[5:]
    bucket, _, prefix = path.partition("/")
    keys = list_objects(bucket, prefix, ext)
    return [f"s3://{bucket}/{k}" for k in keys]


def get_cog_files(directory: str) -> list[str]:
    """Get COG files from directory."""
    cog_extensions = [".tif", ".tiff", ".TIF", ".TIFF"]
    files = []
    for ext in cog_extensions:
        if directory.startswith("s3://"):
            files.extend(get_cog_files_s3(directory, ext))
        else:
            files.extend(get_cog_files_local(directory, ext))
    return sorted(files)


def create_mosaic_json(cog_files: list[str], output_path: Path | None = None) -> dict[str, Any]:
    """Create and optionally save MosaicJSON from COG files."""
    mosaic = MosaicJSON.from_urls(cog_files, minzoom=0, maxzoom=22)
    model = mosaic.model_dump()
    if output_path:
        output_path = Path(output_path)
        with output_path.open("w") as f:
            json.dump(model, f)
    return model
