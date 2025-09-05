# MyTi

<p align="center">
  <img src="assets/myti-logo.png" alt="MyTi logo" width="150"/>
</p>

## Overview

**MyTi** is a web application for hosting and visualising raster **Cloud Optimised GeoTIFFs (COGs)**. It integrates with **Mapbox** for high-resolution basemaps and provides efficient display, caching, and interaction with geospatial raster datasets.

<p align="center">
  <img src="assets/web-app.png" alt="Web application" width="500"/>
</p>

## Installation

1. **Clone the repository**  
   ```bash
   git clone git@github.com:geraldmoore/myti.git
   cd myti
   ```

2. **Set up the Python environment**  
   ```bash
   uv sync
   ```

3. **Configure environment variables**  
   Create a `.env` file in the project root with the following and fill in the values:  
   ```bash
   AWS_PROFILE=
   AWS_REGION=
   MAPBOX_ACCESS_TOKEN=
   ```  
   You may obtain a free Mapbox access token by registering at [Mapbox](https://www.mapbox.com/) and following [these instructions](https://docs.mapbox.com/help/glossary/access-token/). Configuring the AWS profile and region is only
   necessary if your data is stored on S3. Otherwise you can leave these empty.

## Data Preparation

To ensure optimal performance and visual quality:

- **Use COGs:** Convert raster files to Cloud Optimised GeoTIFFs using tools such as `rasterio` or `GDAL`.  
- **Reprojection:** TiTiler renders in Web Mercator (`EPSG:3857`). For multiple tiles, merge and reproject them together to prevent misalignment.  
- **Data type:** Input rasters should be in `uint8` format. If exact pixel values are required, consider alternative platforms such as QGIS.  
- **Transparency:** Configure transparency by setting the `nodata` value in the COG (e.g. `nodata=0.0`).  
- **Reference materials:** Example conversion and formatting code snippets can be found in `workspace.ipynb`.

## Configuration

Before running the application, edit the `config.yaml` file in the project root:

```yaml
name: dataset-name
raster_dir: path-to-directory-containing-rasters
cache_dir: "./cache"
host: "127.0.0.1"
port: 8080
```

- `name` — Identifier for your dataset.  
- `raster_dir` — Directory path or S3 bucket containing raster files.  
- `cache_dir` — Location for intermediate cache files to accelerate reloads.  
- `host` and `port` — Network configuration for serving the web application.  

## Usage

1. **Launch the server**  
   ```bash
   uv run uvicorn app.main:app
   ```  
   This generates a `{name}-mosaic.json` index in the cache directory and starts the TiTiler web server.

2. **Access the application**  
   Open your browser at `http://<host>:<port>` to view the web application.  
   You may toggle between base layers and raster overlays as required.

3. **Caching behaviour**  
   - Cached data enables rapid reloading. Delete the cache directory to regenerate data with updated rasters.  
   - Changing the `name` field in `config.yaml` will create a new dataset cache.  
   - Reusing a previous dataset name will load directly from its existing cache.  

## Additional Resources

- The provided `workspace.ipynb` notebook contains general-purpose code snippets to support data formatting and conversion workflows.
