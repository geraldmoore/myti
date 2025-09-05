# MyTi README

<img src="assets/myti-logo.png" alt="MyTi logo" width="150"/>

## Summary

MyTi is a web application for hosting and visualizing raster Cloud Optimized GeoTIFFs (COGs). It leverages MapBox for high-resolution base layers and supports display and caching of geospatial raster datasets.

<div style="text-align: center;">
  <img src="assets/web-app.png" alt="Web app" width="300"/>
</div>

## Installation

1. Clone the repository:
   ```
   git clone <path-to-github-repo>
   cd myti
   ```

2. Set up the Python environment:
   ```
   uv sync
   ```

3. Configure environment variables:
   - Create a `.env` file in the project root with:
     ```
     AWS_PROFILE=your-aws-profile
     AWS_REGION=your-aws-region
     MAPBOX_ACCESS_TOKEN=your-mapbox-token
     ```
   - Obtain a free MapBox access token by signing up at [MapBox](https://www.mapbox.com/) and following [these instructions](https://docs.mapbox.com/help/glossary/access-token/).

## Data Preparation

- **Use COGs:** Convert raster files to Cloud Optimized GeoTIFFs for efficient loading and visualization. Use `rasterio` or `gdal` for conversion.
- **Reprojection:** TiTiler displays data in WebMercator (`EPSG:3857`). For multiple tiles, merge them into a single file and reproject together to avoid misalignment.
- **Data Type:** Input rasters should be in `uint8` format. If precise pixel values are needed, consider alternative tools like QGIS.
- **Transparency:** Set the `nodata` value in the COG (e.g., `nodata=0.0`) to configure transparent areas.
- **Reference:** See `workspace.ipynb` for code snippets to assist with data formatting and conversion.

## Usage

Edit `config.yaml` in the project root:
```bash
name: dataset-name
raster_dir: path-to-directory-containing-rasters
cache_dir: "./cache"
host: "127.0.0.1"
port: 8080
```

- `name`: Identifier for your dataset.
- `raster_dir`: Directory or S3 path containing raster files.
- `cache_dir`: Stores intermediate files for faster reloads.
- `host` and `port`: Network settings for the web app.

## Usage

1. Start the server:
   ```
   uv run uvicorn app.main:app
   ```
   - This generates a `{name}-mosaic.json` index in the cache directory and launches the TiTiler web server.

2. Access the web app:
   - Visit `http://<host>:<port>` in your browser.
   - Toggle base layers and raster overlays as needed.

3. Caching:
   - Cached data allows fast reloads. Delete the cache directory to refresh with new data.
   - Changing the `name` field in `config.yaml` switches datasets and generates a new cache alongside existing datasets. Reusing a previously cached name will load from the cache.

## Additional Notes

- See the provided `workspace.ipynb` notebook for general useful code snippets.
